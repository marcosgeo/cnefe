# -*- coding: utf-8 -*-
'''
Created on Ago 2, 2018

@author: marcosgeo@yahoo.com
'''
import traceback
from osgeo import ogr
from cnefe.quadra import carregar_quadras

class Distrito:
    def __init__(self, codigo, nome, geom): #construtor
        self.codigo = codigo
        self.nome = nome
        self.quadras = None
        self.geom = ogr.CreateGeometryFromWkt(geom)

    def __repr__(self):
        return u"{} - {}".format(self.codigo, self.nome)    
        
    def geocodificar(self, conexao, setor=None, quadra=None):
        try:
            for quadra in self.quadras:
                print u"Geocodificando quadra {}".format(quadra)
                if not setor:
                    quadra.geocodificar(conexao, self.codigo)
                else:
                    if setor in quadra.condigo:
                        quadra.geocodificar(conexao, self.codigo)
            conexao.commit()
            print u"Concluida geocodificacao {}".format(self)
        except:
            print u"Falha ao geocodificar"
            print traceback.format_exc()
            
    def carregar_quadras(self, conexao):
        """Carrega as quadras e lotes do distrito"""
        self.quadras = carregar_quadras(conexao, self.codigo)
    
    def extrair_lotes(self, conexao):
        """Carrega as quadras extraindo os lotes"""
        self.quadras = carregar_quadras(conexao, self.codigo, 'extrair')
        
    def classificar_atividade(self, conexao):
        """Classifica a atividade dos lotes"""
        try:
            for quadra in self.quadras:
                for face in quadra.faces:
                    print u"Classificando lotes da face {}".format(
                        face)
                    for lote in face.lotes:
                        for termo in lote.estabelecimento.split():
                            if len(termo) < 3: continue
                            for grupo in GRUPOS_ATIVIDADES:
                                for atv in grupo[2].split():
                                    if termo.lower() in atv:
                                        lote.grupo = grupo[0]
                                        break
                                if lote.grupo:
                                    break
                            if lote.grupo:
                                lote.salvar(conexao.cursor())
                                break
            conexao.commit()
            print u"Classificacao da atividade concluida {}".format(
                self )
            return True
        except:
            print u"Nao foi possivel classificar a atividade"
            print traceback.format_exc()
            return False
    
    
def carregar_distritos(conexao, cod_muni, modo = 'carregar'):
    
    try:
        distritos = []
        cursor = conexao.cursor()
        cursor.execute(SQL_DIST, (cod_muni,))
        dist = cursor.fetchone()
        while dist:
            distrito = Distrito(dist[0], dist[1], dist[2])
            if modo == 'carregar':
                distrito.carregar_quadras(conexao)
            elif modo == 'extrair':
                distrito.extrair_lotes(conexao)

            distritos.append(distrito)
            
            dist = cursor.fetchone()

        return distritos
    except:
        print "Nao foi possivel carregar os distritos"
        print traceback.format_exc()
        return None
    finally:
        if cursor:
            cursor.close()

GRUPOS_ATIVIDADES = [
        ('A', 'alimentação', 'restaurantes, lanchonetes, bares'),
        ('B', 'abastecimento', 'padarias, mercado, supermercado, hipermercado'),
        ('C', 'instituição cultural', 'museu, biblioteca, outros'),
        ('D', 'lojas de departamento', 'equipamento comercial, shopping, galeria'+\
            ', lojas departameno', 'efificio comercial'),
        ('E', 'entretenimento', 'boate, teatro, cinema, boliche'),
        ('F', 'finanças', 'bancos, casa de cambio, factoring, loteria'),
        ('G', 'atividade de calçada', 'banca de jornal, frutas, flores, doces'),
        ('H', 'hospedagem', 'hotel, pousada, hostel, pensao'),
        ('I', 'imóveis vagos', 'salas, edificações, terrenos, construcao'),
        ('J', 'equipagem', 'eletronicos, moveis'),
        ('K', 'escritório', 'contabilidade, advocacia, marketing, turismo'+\
            ', comunicacao'),
        ('L', 'vestuário', 'vestuario feminino, masculino, infantil, moda'),
        ('M', 'artigos pessoais', 'acessorios, decoracao, sapataria, joalheria'+\
            ', perfumaria, farmacia, otica, quinquilharias'),
        ('N', 'educação e treinamento', 'escola, universidade, faculdades'+\
            ', treinamento, curso'),
        ('O', 'serviços especializados', 'lavanderia, lava, jato, rapido'),
        ('P', 'serviço pesado', 'mecanica, ferragem, ferragens, conserto maquinas'),
        ('Q', 'medicina', 'laboratorios, consultorios, hospital'),
        ('R', 'repartições públicas', 'federeal, estadual, municipal'),
    ]
SQL_DIST = """
SELECT cd_geocodd, nm_distrit, st_astext(geom)
FROM censo2010.distritos
WHERE substr(cd_geocodd, 1, 7) = %s 
    and cd_geocodd in ('355030815', '355030871', '355030816');
"""
SQL_LOTES = """
SELECT gid, setor_id, quadra, face, especie,
    estab_nome, lograd_tipo, lograd_tit, lograd_nome, 
    imovel_numero, modificador, unidades, andares,
    aptos_andar, testada, cep, indicador, grupo,
    geom
WHERE setor_id like %s;
"""