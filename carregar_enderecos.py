#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 03, 2018

@author: marcosgeo@yahoo.com
'''
import os.path
import time
import zipfile
import traceback

from utils.conexao import conexao
from utils.utils import remove_acentos
from cnefe.endereco import Endereco

char_code = 'latin1'
def carregar_enderecos(cursor, pasta_txt, arquivo, pasta_log):
    zarquivo = zipfile.ZipFile(os.path.join(pasta_txt,arquivo), 'r')
    
    for nome in zarquivo.namelist():
        txt = zarquivo.open(nome)
        log_nome = os.path.join(pasta_log, arquivo[:-3]+"txt")
        log = open(log_nome, 'w')
        msg = u"\n{} - Carregando arquivo {}".format(time.strftime("%x %X"), nome)
        print(msg)
        log.write(msg)
        i = 0
        erro = "sem erros"
        for linha in txt.readlines():
            i += 1
            try:
                endereco = Endereco(linha)
                cursor.execute( SQL_INSERT, (
                    endereco.uf, endereco.municipio, endereco.distrito, endereco.subdistrito,
                    endereco.setor_id, endereco.setor_cod, endereco.setor_sit, endereco.quadra,
                    endereco.face, endereco.especie, endereco.lograd_tipo, endereco.lograd_titulo,
                    endereco.lograd_nome, endereco.imovel_numero, endereco.modificador,
                    endereco.elemento1, endereco.valor1, endereco.elemento2, endereco.valor2,
                    endereco.elemento3, endereco.valor2, endereco.elemento4, endereco.valor4,
                    endereco.elemento5, endereco.valor5, endereco.elemento6, endereco.valor6,
                    endereco.latitude, endereco.longitude, endereco.localidade,
                    remove_acentos(endereco.nome_estab.decode(char_code)), endereco.indicador, 
                    endereco.domicilio_coletivo, endereco.cep))
            except:
                msg = u"\n{} - Erro: {}Linha {}: {}".format(
                    time.strftime("%x %X"), traceback.format_exc(), i, 
                    remove_acentos(linha.decode(char_code)))
                log.write(msg)
                erro = "com erros"
                print traceback.format_exc()
                cursor.connection.rollback()
                break

        cursor.connection.commit()
        msg = u"{} - Carga concluida {}.".format(time.strftime("%x %X"), erro)
        log.write(msg)
        log.close()
        print msg
        
def iniciar():
    try:
        con = conexao()
        
        distritos = ['3550308']
        
        pasta_txt = r"./ibge/cnefe/txt/"
        pasta_log = r"./ibge/cnefe/log/"
        cursor = con.cursor()
        
        arquivos = os.listdir(pasta_txt)
        for arquivo in arquivos:
            for d in distritos:
                if d in arquivo:
                    carregar_enderecos(cursor, pasta_txt, arquivo, pasta_log)
                    break
    except:
        print(traceback.format_exc())
    finally:
        if con:
            con.close()


    
SQL_INSERT = u"""
insert into censo2010.cnefe_enderecos(
        uf_cod, muni_cod, distrito, subdistrito, setor_id, setor_cod, setor_sit,
        quadra_num, face_num, especie, lograd_tipo, lograd_tit, lograd_nome, 
        imovel_numero, modificador, comp_elem1, comp_valor1, comp_elem2, 
        comp_valor2, comp_elem3, comp_valor3, comp_elem4, comp_valor4, 
        comp_elem5, comp_valor5, comp_elem6, comp_valor6, latitude, 
        longitude, localidade, nome_estab, indicador, coletivo, cep)
values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
if __name__ == "__main__":
    iniciar()