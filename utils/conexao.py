'''
Created on Jun 4, 2018

@author: marcosgeo@yahoo.com
'''
import psycopg2
from psycopg2.extras import DictCursor

def conexao():
    return psycopg2.connect(
        "host=localhost port=5432 dbname=ibge user=postgres password=.senha.",
        cursor_factory=DictCursor)
