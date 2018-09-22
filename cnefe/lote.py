# -*- coding: utf-8 -*- 

'''
Created on Jun 3, 2018

@author: marcosgeo@yahoo.com
'''

import traceback
from shapely import wkt

# campos do endereco a serem analizados para extrair bloco e andar
CAMPOS = ['comp_elem1', 'comp_elem2', 'comp_elem3', 'comp_elem4', 'comp_elem5', 'comp_elem6']
VALORES =['comp_valor1', 'comp_valor2', 'comp_valor3', 'comp_valor4', 'comp_valor6', 'comp_valor6']

class Lote:
    """Representa um lote a partir de informacoes extraidas do CNEFE."""

    def __init__(self, end): #construtor
        self.gid = end['gid'] if 'gid' in end else None
        self.setor = end['setor_id'].strip()
        self.quadra = end['quadra_num']
        self.face = end['face_num']
        self.especie = end['especie']
        self.estabelecimento = end['nome_estab'].strip()
        self.lograd_tipo = end['lograd_tipo'].strip()
        self.lograd_tit = end['lograd_tit'].strip()
        self.lograd_nome = end['lograd_nome'].strip()
        self.numero = end['imovel_numero']
        self.modificador_num = end['modificador'].strip()
        self.cep = end['cep'].strip()
        self.indicador = end['indicador'].strip()
        self.grupo = end['grupo'] if 'grupo' in end else None
        self.quant_edificacoes = 1
        self.unidades = end['unidades'] if 'unidades' in end else 1
        self.fator = 1
        self.blocos = end['blocos'].split() if 'blocos' in end else []
        self.andares = end['andares'] if 'andares' in end else 0
        self.aptos_andar = 0
        self.altura = None
        self.testada = end['testada'] if 'testada' in end else None
        self.posicao = end['posicao'] if 'posicao' in end else 0
        self.ponto = wkt.loads(end['geom']) if 'geom' in end else None

    def salvar(self, cursor):
        """Salva o lote no banco de dados."""
        
        try:
            if not self.gid:
                cursor.execute(SQL_INSERT, (
                    self.setor, self.quadra, self.face, self.especie, 
                    self.estabelecimento,self.lograd_tipo, self.lograd_tit, self.lograd_nome, 
                    self.numero, self.modificador_num, self.unidades, self.andares,
                    self.aptos_andar, self.testada, self.cep, self.indicador,
                    self.grupo, self.ponto.wkt))
                return cursor.rowcount
            else:
                cursor.execute(SQL_UPDATE, (self.setor, self.quadra, self.face,
                    self.especie, self.indicador, self.estabelecimento, 
                    self.lograd_tipo, self.lograd_tit, self.lograd_nome, 
                    self.numero, self.modificador_num, self.cep, self.unidades, 
                    self.andares, self.aptos_andar, self.testada, self.posicao, 
                    self.grupo,self.ponto.wkt, self.gid,))
                return cursor.rowcount
        except:
            print traceback.format_exc()
            cursor.rollback()
            return 0
   
    def incluir_endereco(self, end):
        
        if self.numero == end['imovel_numero']:
            if self.modificador_num == end['modificador']:
                self.unidades += 1
                
                self.extrair_bloco(end)
                self.extrair_andar(end)
                return True
        
        return False
    
    def extrair_bloco(self, end):
        """Verifica e extrai um bloco de um endereco"""
        
        termos = ['BLOCO', 'PREDIO', 'EDIFICIO', 'TORRE', 'ANEXO']

        bloco = None    
        for termo in termos:
            for i, campo in enumerate(CAMPOS):
                if termo in end[campo]:
                    bloco = end[VALORES[i]]
                    break
            if bloco: break
        
        if bloco and bloco not in self.blocos:
            self.blocos.append(bloco)
            
            return True
        else:
            return False
    
    def extrair_andar(self, end):
        """Verifica e extrai o andar de um endereco"""
        
        termos = ['ANDAR', 'PAVIMENTO']
        andar = 0
        aptos_andar = 0
        extraiu = None
        try:
            for termo in termos:
                for i, campo in enumerate(CAMPOS):
                    if termo in end[campo]:
                        try:
                            andar = int(end[VALORES[i]])
                            extraiu = False
                            break
                        except:
                            andar = 0
                if andar > 0: break
            if andar == 0: # tenta obter o andar a partir do numero do apto
                for i, campo in enumerate(CAMPOS):
                    if 'APARTAMENTO' in end[campo] or 'APTO' in end[campo]:
                        try:
                            if len(end[VALORES[i]]) == 2:
                                andar = int(end[VALORES[i]][0])
                                aptos_andar = int(end[VALORES[i]][1])
                                extraiu = False
                                break
                            elif len(end[VALORES[i]]) >= 3:
                                andar = int(end[VALORES[i]][0:2])
                                aptos_andar = int(end[VALORES[i]][2:])
                                extraiu = False
                                if andar > 50:
                                    andar = int(end[VALORES[i]][0:1])
                                    aptos_andar = int(end[VALORES[i]][1:])
                                break
                        except:
                            andar = 0
                            aptos_andar = 0
            if andar > self.andares:
                self.andares = andar
                extraiu = True
            if aptos_andar > self.aptos_andar:
                self.aptos_andar = aptos_andar
            if type(andar) == str or type(aptos_andar)== str:
                pass
            return extraiu
        
        except:
            print(traceback.format_exc())
            return extraiu
    
    def __unicode__(self):
        return u"'{}{},  {}'".format(self.numero, self.modificador_num, 
                                   self.lograd_nome)
    def __repr__(self):
        return u"'{}{},  {}'".format(self.numero, self.modificador_num, 
                                   self.lograd_nome)
        
SQL_INSERT = """
insert into censo2010.cnefe_lotes(
    setor_id, quadra, face, especie,
    estab_nome, lograd_tipo, lograd_tit, lograd_nome, 
    imovel_numero, modificador, unidades, andares,
    aptos_andar, testada, cep, indicador, grupo,
    geom)
values(
    %s, %s, %s, %s,
    %s, %s, %s, %s, 
    %s, %s, %s, %s,
    %s, %s, %s, %s, %s,
    st_geomfromtext(%s, 4674)
);"""

SQL_UPDATE = """
UPDATE censo2010.cnefe_lotes
SET setor_id=%s, quadra=%s, face=%s, especie=%s, indicador=%s, 
    estab_nome=%s, lograd_tipo=%s, lograd_tit=%s, lograd_nome=%s,
    imovel_numero=%s, modificador=%s, cep=%s, unidades=%s, andares=%s,
    aptos_andar=%s, testada=%s, posicao=%s, grupo=%s, 
    geom=st_geomfromtext(%s, 4674)
WHERE gid=%s;"""
