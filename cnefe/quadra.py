# -*- coding: utf-8 -*-
'''
Created on Jun 4, 2018

@author: marcosgeo@yahoo.com
'''
import time
import traceback
import psycopg2.extras

from face import carregar_faces

class Quadra:
    
    def __init__(self, cod, setor, num): #construtor
        self.codigo = cod
        self.setor = setor
        self.numero = int(num)
        self.faces = []
        self.geom = None
    
    def __repr__(self):
        return u"{} - {}".format(self.setor, self.numero)

    def salvar(self, conexao):
        sql_insert = u"""
        insert into censo2010.cnefe_quadras(codigo, setor, numero, geom)
        values(%s, %s, %s, st_geomfromtext(%s, 4674));
        """
        try:
            cursor = conexao.cursor()
            instrucao = sql_insert.format(self.codigo, self.setor, self.numero, 
                                          self.geom)
            cursor.execute(instrucao)
            cursor.connection.commit()
            return cursor.rowcount
        except:
            print(traceback.format_exc())
            return 0
        finally:
            if cursor:
                cursor.close()
    
    def carregar_faces(self, conexao, modo='carregar'):
        """Recupera as faces da quadra"""
        self.faces = carregar_faces(conexao, self.setor, self.numero, modo)
        return True
    

    def get_face(self, face):
        for f in self.faces:
            if f.numero == face:
                return f
        else:
            return None
    
    def geocodificar(self, conexao, setor=None, numero=None):
        """Interpola os enderecos de uma quadra em suas respectivas faces."""
        try:
            erros = 0
            info = 0
            log = u"Setor: {}, Quadra: {}".format(self.setor, self.numero)
            info_log = log
            for i, face in enumerate(self.faces):
                if len(face.lotes) == 0:
                    face.carregar_lotes(conexao)
                inicio = None
                    # verifica a ordem de caminhamento da face
                if i < len(self.faces)-1:
                    inicio = face.get_inicio(self.faces[i+1])
                else:
                    inicio = face.get_inicio(self.faces[0])
                
                erros  = face.geocodificar(conexao, inicio)
                
            return [erros, log, info, info_log]
        except:
            print(traceback.format_exc())
            return False

def carregar_quadras(conexao, distrito, modo='carregar'):
    """Carrega as quadras de um distrito"""
    try:
        quadras = []
        cursor = conexao.cursor()
        cursor.execute(SQL_QUADRAS, (distrito,))
        registro = cursor.fetchone()
        while registro:
            quadra = Quadra(registro[1], registro[2], registro[3])
            quadra.carregar_faces(conexao, modo)
            quadras.append(quadra)
            registro = cursor.fetchone()
        
        return quadras
    finally:
        if cursor:
            cursor.close()

SQL_QUADRAS = """
SELECT gid, codigo, setor, numero
  FROM censo2010.cnefe_quadras
WHERE substr(setor, 1, 9) = %s
"""
