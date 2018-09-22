# -*- coding: utf-8 -*-
'''
Created on Jun 3, 2018

@author: marcosgeo@yahoo.com
'''
import traceback
from copy import deepcopy
from time import strftime
from shapely import wkt
from lote import Lote

class Face:
    """Representa uma face de quadra"""
    def __init__(self, face): #construtor
        self.id = face['id']
        self.codigo = face['codigo']
        self.setor = face['setor']
        self.quadra = int(face['quadra'])
        self.numero = int(face['face'])
        self.lograd_tipo = face['lograd_tipo']
        self.lograd_titulo = face['lograd_titulo']
        self.lograd_nome = face['lograd_nome'].replace("'","`")
        self.residencias = face['residencias']
        self.imoveis = face['imoveis']
        self.tipo = face['tipo']
        self.lotes = []
        self.geom = wkt.loads(face['geom'])
        self.extensao = self.geom.length * 100000
        self.num_ini = 0
        self.num_fim = 0
        self.posicoes = 0
        self.inicio = None
    def __repr__(self):
        return u"{} - {} - {}".format(self.setor, self.quadra, self.numero)
    
    def salvar(self,conexao):
        """Armazena o registro na tabela"""
        SQL_INSERT = u"""
        insert into censo2010.cnefe_faces(
            id, codigo, setor, quadra, face, lograd_tipo, lograd_titulo,
            lograd_nome, residencias, imoveis, tipo, geom)
        values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            st_geomfromtext(%s, 4674));
        """
        try:
            cursor = conexao.cursor()
            cursor.execute(SQL_INSERT, (
                self.id, self.codigo, self.setor, self.quadra, self.numero,
                self.lograd_tipo, self.lograd_titulo, self.lograd_nome,
                self.residencias, self.imoveis, self.tipo, self.geom.wkt
            ))
            return cursor.rowcount
        except:
            print(traceback.format_exc())
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def get_ordem(self):
        """Define se a ordem de percorrimento da quadra foi crescente ou decrescente"""
        if len(self.lotes) > 1:
            if self.lotes[0].numero < self.lotes[self.posicoes-1].numero:
                return "crescente"
            else:
                return "descrescente"
        else:
            return False
    
    
    
    def incluir_lote(self, lote):
        """Inclui um lote na face"""
        
        if self.num_fim == 0 or lote.numero > self.num_fim:
            self.num_fim = lote.numero
        if self.num_ini == 0 or lote.numero < self.num_ini:
            self.num_ini = lote.numero
        
        self.posicoes += 1
        lote.posicao = self.posicoes
        
        if lote.andares > 20:
            lote.fator = 4
        elif lote.andares > 15:
            lote.fator = 3
        elif lote.andares > 5:
            lote.fator = 2
        elif lote.especie in [4, 5]:
            lote.fator = 5
            
        self.lotes.append(lote)
        
    def get_total_lotes(self):
        return len(self.lotes)

    def get_testada(self):
        total = 0
        for lote in self.lotes:
            total += lote.fator
        return self.extensao / total
    
    def get_testada_g(self):
        try:
            total = 0
            for lote in self.lotes:
                total += lote.fator
                
            return self.geom.length / total
        except:
            #print(traceback.format_exc())
            return 0
        
    def get_inicio(self, outra):
        """Retorna o primeiro vertice da ordem de caminhamento da face."""
        g1_ult = self.geom.coords[-1]
        g2_prim = outra.geom.coords[0]
        g2_ult = outra.geom.coords[-1]
        
        # sendo o ultimo vertice o de contato com a outra face,
        # o inicio da face esta no primeiro vertice
        if g1_ult == g2_prim or g1_ult == g2_ult:
            return 0
        else: # caso contrario esta no ultimo
            return len(self.geom.coords) - 1
    
    def extrair_lotes(self, conexao):
        """Analisa os enderecos de uma face e os transforma em lotes."""
        try:

            cursor = conexao.cursor()
            cursor.execute(SQL_ENDERECOS,(
                self.setor, int(self.quadra), int(self.numero)))
            end = cursor.fetchone()
            lote = None

            while end:
                if lote:
                    if not lote.incluir_endereco(end):
                        self.incluir_lote(lote)
                        # cria novo lote
                        lote = Lote(end)
                else:
                    lote = Lote(end)
                
                end = cursor.fetchone()
            if lote:
                self.incluir_lote(lote)
                return True
            else:
                return False
        except:
            return False
        finally:
            if cursor:
                cursor.close()

    def geocodificar(self, conexao, inicio):
        """
        Geocodifica, por interpolacao, os lotes da face
        """
        try:
            log = ""
            info = 0
            fator_acumulado = 0
            extensao_face = self.geom.length
            testada_face = self.get_testada_g()
            # se a face nao possui testada padrao ela nao tem lotes
            if testada_face == 0:
                log += u"\n{} - Face sem lotes. Face: {}".format(
                    strftime("%x %X"), self.codigo)
                info += 1
                
            cursor = conexao.cursor()
            # calcula a localizacao do lote na face
            for lote in self.lotes:
                fator_acumulado += lote.fator - 1
                testada_lote = testada_face * lote.fator
                posicao = lote.posicao + fator_acumulado
                perc = (( posicao * testada_face) - (testada_lote / 2)) / extensao_face
                ponto = None
                try:
                    # se inicia em 0 e porque a ordem dos vertices esta 
                    # no mesmo sentido do caminhamento da face
                    if inicio == 0:
                        ponto = self.geom.interpolate( perc, normalized = True)
                    else:
                        ponto = self.geom.interpolate( 1 - perc, normalized = True)
    
                except:
                    log += u"\n{} - Nao foi possivel gerar uma geometria para o "+\
                        u"lote {}:{}:{}-{}. Erro: {}".format(
                        strftime("%X %X"), lote.setor, lote.quadra, lote.face, lote.numero,
                        traceback.format_exc()
                        )
                    continue
                
                lote.ponto = ponto
                
                lote.testada = self.extensao / self.get_total_lotes()
                lote.blocos = ", ".join(lote.blocos)
    
                try:
                    lote.salvar(cursor)
                except:
                    log += u"\n{} - Erro ao salvar o lote {}:{}:{}-{}. Erro: {}".format(
                        strftime("%x %X"), lote.setor, lote.quadra, lote.face,
                        lote.numero, traceback.format_exc())
                    continue
            
            return True
        finally:
            if cursor:
                cursor.connection.commit()
                cursor.close()
        
    def carregar_lotes(self, conexao):
        """Carregar os lotes da faces para a memoria"""
        try:
            cursor = conexao.cursor()
            cursor.execute(SQL_LOTES, (self.setor, self.quadra, self.numero,))
            
            registro = cursor.fetchone()
            while registro:
                lote = Lote(registro)
                self.lotes.append(deepcopy(lote))
                
                registro = cursor.fetchone()
            
            cursor.close()
            return True
        except:
            print traceback.format_exc()
            return False
        
def carregar_faces(conexao, setor, quadra, modo='carregar'):
        """Recupera as faces da quadra"""
        try:
            faces = []
            cursor = conexao.cursor()
            cursor.execute(SQL_FACES, (setor, quadra,))
            
            registro = cursor.fetchone()
            while registro:
                face = Face(registro)
                faces.append(face)
                if modo == 'carregar':
                    face.carregar_lotes(conexao)
                elif modo == 'extrair':
                    face.extrair_lotes(conexao)
                    
                registro = cursor.fetchone()
            
            cursor.close()
            return faces 
        except:
            print(traceback.format_exc())
            return faces
        finally:
            if cursor:
                cursor.close()
        
SQL_ENDERECOS = u"""
select id, uf_cod, muni_cod, distrito, subdistrito, setor_cod, setor_sit,
    setor_id, quadra_num, face_num, especie, lograd_tipo,
    lograd_tit, lograd_nome, imovel_numero, modificador, comp_elem1,
    comp_valor1, comp_elem2, comp_valor2, comp_elem3, comp_valor3,
    comp_elem4, comp_valor4, comp_elem5, comp_valor5, comp_elem6,
    comp_valor6, latitude, longitude, localidade, nome_estab,
    indicador, coletivo, cep
from censo2010.cnefe_enderecos
where setor_id = %s and quadra_num = %s and face_num = %s
order by ordem ;
"""

SQL_FACES = u"""
select gid, st_astext(geom) geom, id, codigo, setor, quadra, face,
    lograd_tipo, lograd_titulo, lograd_nome, residencias, imoveis, tipo
from censo2010.cnefe_faces
where setor = %s and quadra = %s
order by face;
"""

SQL_LOTES = u"""
SELECT gid, setor_id, quadra quadra_num, face face_num, especie, 
       indicador, estab_nome nome_estab, lograd_tipo, lograd_tit, lograd_nome,
       imovel_numero, modificador, cep, unidades, andares, aptos_andar, 
       testada, posicao, grupo, st_astext(geom) geom
  FROM censo2010.cnefe_lotes
  WHERE setor_id = %s and quadra = %s and face = %s
  ORDER BY posicao;
"""