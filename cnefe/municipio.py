# -*- coding: utf-8 -*- 
'''
Created on Ago 2, 2018

@author: marcosgeo@yahoo.com
'''
from osgeo import ogr
from distrito import carregar_distritos

class Municipio:
    
    def __init__(self, geocodm, nome, geom): #construtor
        self.geocodm = geocodm
        self.nome = nome
        self.distritos = []
        self.geom = ogr.CreateGeometryFromWkt(geom)

        
    def geocodificar(self, conexao, distrito=None, setor=None, quadra=None):
        try:
            cursor = conexao.cursor()
            if not distrito:
                for dist in self.distritos:
                    dist.geocodificar(cursor, setor, quadra)
            else:
                for dist in self.distritos:
                    if dist.cod == distrito:
                        dist.geocodificar(cursor, setor, quadra)
        finally:
            if not cursor.closed:
                cursor.close()
                
    def classificar_atividade(self, cursor):
        """Classifica os ramos de atividade dos lotes"""
        
        
def carregar(conexao, geocodm, modo='carregar'):
    try:
        cursor = conexao.cursor()
        cursor.execute(SQL_MUNI,(geocodm,))
        result = cursor.fetchone()
        if result:
            municipio = Municipio(result[0], result[1], result[2])
            distritos = carregar_distritos(conexao, result[0], modo)
            if distritos:
                municipio.distritos = distritos
            print u"Municipio carregado com sucesso"
            return municipio
        else:
            print u"\nNão existe o municipio indicado"
            return None
    except:
        print u"Erro ao tentar carregar o municipio indicado"
        return None
    finally:
        if not cursor.closed:
            cursor.close()

SQL_MUNI = """
SELECT cd_geocodm, nm_municip, st_astext(geom)
FROM censo2010.municipios
WHERE cd_geocodm = %s;
"""