#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 22, 2018

@author: marcosgeo@yahoo.com
'''


import os
import time
import traceback

from osgeo import ogr
from utils.conexao import conexao

def carregar_municipios(pasta, arquivo):
    
    con = None
    try:
        con = conexao()
        cursor = con.cursor()
        sql_insere = u"""
            insert into censo2010.municipios
                (cd_geocodm, nm_municip, geom)
                values (%s, %s, st_geomfromtext(%s, 4674));
            """
        shape_ds = ogr.Open(os.path.join(pasta, arquivo), 0)
        for feature in shape_ds.GetLayer():

            if feature.GetField('CD_GEOCODM'):
                cursor.execute(sql_insere, (
                    feature.GetField('CD_GEOCODM'),
                    feature.GetField('NM_MUNICIP').decode('utf-8'),
                    feature.geometry().ExportToWkt())
                )
        con.commit()
        print("\n{} - Municipios importados com sucesso".format(
            time.strftime("%x %X")))
    except:
        print(traceback.format_exc())
    finally:
        if con:
            con.close()
    
def carregar_distritos(pasta, arquivo):
    
    con = None
    try:
        con = conexao()
        cursor = con.cursor()
        sql_insere = u"""
            insert into censo2010.distritos
                (cd_geocodd, nm_distrit, geom)
                values (%s, %s, st_geomfromtext(%s, 4674));
            """
        shape_ds = ogr.Open(os.path.join(pasta, arquivo), 0)
        for feature in shape_ds.GetLayer():
            if feature.GetField('CD_GEOCODD'):
                cursor.execute(sql_insere, (
                    feature.GetField('CD_GEOCODD'),
                    feature.GetField('NM_DISTRIT').decode('utf-8'),
                    feature.geometry().ExportToWkt())
                )
        
        con.commit()
        print("\n{} - Distritos importados com sucesso".format(
            time.strftime("%x %X")))
    except:
        print(traceback.format_exc())
    finally:
        if con:
            con.close()

if __name__ == "__main__":
    
    pass
