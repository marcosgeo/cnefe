#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jun 10, 2018

@author: marcosgeo@yahoo.com
'''

import os
import sys
import time
import zipfile
import shutil
import traceback
from osgeo.ogr import Open
from shapely import wkt

from cnefe.quadra import Quadra
from cnefe.face import Face
from utils.conexao import conexao


def salvar_setor(conexao, shp):
    u"""Salva os setores censitarios"""
    SQL_SETOR = u"""
    insert into censo2010.cnefe_setores(
        id, geocod, tipo, geocodb, bairro, geocodd, distrito,
        geocods, subdistrito, geocodm, municipio, mesoregiao, microregiao,
        geom)
    values ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
        st_geomfromtext(%s, 4674));
    """
    
    try:
        cursor = conexao.cursor()
        setores = Open(shp,0)
        
        for setor in setores.GetLayer():
            geom = setor.geometry()
            if geom.GetGeometryName() != 'POLYGON' \
            or geom.GetGeometryRef(0).GetPointCount() < 3:
                continue

            try:
                ident = setor.GetField('ID1')
                geocodi = setor.GetField('CD_GEOCODI')
                tipo = setor.GetField('TIPO')
                geocodb = setor.GetField('CD_GEOCODB')
                bairro = setor.GetField('NM_BAIRRO')
                geocodd = setor.GetField('CD_GEOCODD')
                distrito =   setor.GetField('NM_DISTRIT')
                geocods = setor.GetField('CD_GEOCODS')
                subdist = setor.GetField('NM_SUBDIST')
                geocodm =  setor.GetField('CD_GEOCODM')
                municip = setor.GetField('NM_MUNICIP')
                meso = setor.GetField('NM_MESO')
                micro = setor.GetField('NM_MICRO')
                
                cursor.execute(  SQL_SETOR , (
                    ident, geocodi, tipo,geocodb, bairro, geocodd, distrito, geocods, 
                    subdist, geocodm, municip, meso, micro, geom.ExportToWkt())
                )
            except:
                print traceback.format_exc()
                print("{} - Falha ao salvar setor.".format(time.strftime("%x %X")))
                continue
        cursor.close()
    except:
        print(traceback.format_exc())
    
def processar_quadras(shp, arquivo_log):
    u"""Cria quadras e suas respectivas faces. Salva as faces no banco de dados."""
    try:
        log = open(arquivo_log, "w")
        faces_ds = Open(shp, 0)
        quadras = []
        face = None
        msg = u"{} - Criando quadras do arquivo {}".format(
            time.strftime("%x %X"), shp)
        print msg
        log.write(msg)
        for feature in faces_ds.GetLayer():
            geom = feature.geometry()
            if feature.GetField('ID') > 0 and geom:
                face_atr = {
                    'id': feature.GetField('ID'),
                    'codigo': feature.GetField('CD_GEO'),
                    'setor': feature.GetField('CD_SETOR'),
                    'quadra': feature.GetField('CD_QUADRA'),
                    'face': feature.GetField('CD_FACE'),
                    'lograd_tipo': feature.GetField('NM_TIPO_LO'),
                    'lograd_titulo': feature.GetField('NM_TITULO_'),
                    'lograd_nome': feature.GetField('NM_NOME_LO'),
                    'residencias': feature.GetField('TOT_RES'),
                    'imoveis': feature.GetField('TOT_GERAL'),
                    'geom': geom.ExportToWkt(),
                    'tipo': 'f'
                }
            
                try:
                    face = Face(face_atr)
                except:
                    msg =u"\nID: {}. Nao foi possivel criar a face.".format(
                        face.id, face_atr)
                    log.write(msg)
                    continue
            
                if face.geom.type != 'LineString':
                    msg = u"""\nID: {}. Geometria multipla encontrada. "+\
                        "Forcando geometria unica.""".format(face.id)
                    log.write(msg)
                    #print(msg)
                    face.geom = wkt.loads(geom.GetGeometryRef(0).ExportToWkt())
            
                if feature.GetField('CD_GEO'):
                    
                    q_cod = feature.GetField('CD_GEO').strip()[:-3]
                    q_setor = feature.GetField('CD_SETOR').strip()
                    q_num = feature.GetField('CD_QUADRA').strip()
                    
                    quadra = Quadra(q_cod, q_setor, q_num)
                    
                    existe = False
                    for q in quadras:
                        if quadra.codigo == q.codigo:
                            existe = True
                            quadra = q
                            break
                    if not existe:
                        quadras.append(quadra)
                    
                    quadra.faces.append(face)
                
                else:
                    msg = u"\n{} - Face sem codigo. ID: {}, CD_GEO: {}".format(
                        time.strftime("%x %X"), feature.GetField('ID'), feature.GetField('CD_GEO'))
                    log.write(msg)
                    continue
            else:
                msg = u"\n{} - Registro nao possui identificador ou geometria."
                log.write(msg.format(time.strftime("%x %X")))
                
        msg = u"\n{} - Quadras e faces criadas com sucesso."
        msg = msg.format( time.strftime("%x %X"))
        log.write(msg)
        log.close()
        return quadras
    
    except:
        print traceback.format_exc()
        return False
        
    
def inserir_quadras(conexao, quadras, arquivo_log):
    u"""Insere as quadras e faces no banco de dados"""
    try:
        SQL_QUADRA = u"""
        insert into censo2010.cnefe_quadras (codigo, setor, numero)
        values (%s, %s, %s);
        """
        cursor = conexao.cursor()
        log = open(arquivo_log, "w")
        for q in quadras:
            q.faces.sort(key=lambda face:face.numero)
            for i, face in enumerate(q.faces):
                inicio = None
                
                # busca o vertice de inicio do caminhamento da face
                if i < len(q.faces) -1:
                    inicio = face.get_inicio(q.faces[i+1])
                else:
                    inicio = face.get_inicio(q.faces[0])
                
                # define o vertice de inicio da face em relacao ao caminhamento
                face.inicio = inicio
                face.salvar(conexao)
            try:
                cursor.execute(SQL_QUADRA, (q.codigo, q.setor, q.numero))
                log.write(u"\n{} - Quadra {} inserida com sucesso".format(
                    time.strftime("%x %X"), q.codigo))
            except:
                log.write(traceback.format_exc())
    except:
        log.write(traceback.format_exc())
    finally:
        if cursor:
            cursor.close()
        log.close()
    
def carregar(conexao, shp, shape_log, script_log):
    try:
        log = open(script_log, "a")
        
        if 'face' in shp:
            # cria as quadras e faces a partir do shapefile. salva as faces
            quadras = processar_quadras(shp, shape_log.format("face"))
            if quadras:
                
                quadras_log = shape_log.format("quadras")
                # salva as quadras
                inserir_quadras(conexao, quadras, quadras_log)
                
                log.write(u"\n{} - Terminado {} sem erro.".format(time.strftime("%x %X"), shp))
                
            else:
                
                log.write(u"\n{} - Layer {} nao possui faces com atributos.".format(
                    time.strftime("%x %x"), shp))
            
        if 'setor' in shp:
            log = open(script_log, "a")
            salvar_setor(conexao, shp)
    except:
        print traceback.format_exc()
    finally:
        log.close()
    
def carregar_faces(conexao, nome, pasta_zip, pasta_temp, pasta_log):
    """Processa a arquivo de faces e cria quadras e faces."""
    znome = os.path.join(pasta_zip, nome)
    if os.path.isfile(znome) and 'zip' in znome[-3:]:
        zarquivo = zipfile.ZipFile(znome, 'r')
    else:
        return

    zarquivo.extractall(pasta_temp)
    
    extraidos = os.listdir(pasta_temp)
    for shp in extraidos:
        shp_nome = shp.split("_")[0]
        if shp_nome +'_face.shp' == shp or shp_nome +'_setor.shp' == shp:
            shapefile = pasta_temp + shp
            shape_log = pasta_log + shp[:-4]+"_{}.txt"
            script_log = pasta_log + os.path.basename(sys.argv[0])[:-2]+"txt"
            
            carregar(conexao, shapefile, shape_log, script_log)
            #break
    shutil.rmtree(pasta_temp)
    
def iniciar():
    try:
        con = conexao()
            
        pasta_zip = r"./ibge/cnefe/shp"
        pasta_log = r"./ibge/cnefe/log/"
        pasta_temp = r'./temp/tmp/'
        arquivos = os.listdir(pasta_zip)
        arquivos.sort()
        
              
        for nome in arquivos:
            carregar_faces(con, nome, pasta_zip, pasta_temp, pasta_log)
        con.commit()
        print "{} - Quadras e faces de quadra carregadas com sucesso.".format(
            time.strftime("%x %X"))
    except:
        print traceback.format_exc()
    finally:
        if con:
            con.close()
        
if __name__ == "__main__":
    iniciar()
    