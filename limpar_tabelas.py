# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2018

@author: marcos
'''
from utils.conexao import conexao
def limpar_tabelas():
    """Limpa as tabelas do banco de dados"""
    con = None
    try:
        con = conexao()
        cursor = con.cursor()
        instrucoes = [u"delete from censo2010.cnefe_enderecos",
                      u"delete from censo2010.cnefe_lotes",
                      u"delete from censo2010.cnefe_faces",
                      u"delete from censo2010.cnefe_quadras",
                      u"delete from censo2010.cnefe_setores",
                      u"delete from censo2010.municipios",
                      u"delete from censo2010.distritos"
                    ]
        
        for instr in instrucoes:
            cursor.execute(instr)
            print("\nTabela {} limpa com sucesso.".format(
                instr.split(" ")[2]))
        con.commit()
        
    finally:
        if con:
            con.close()