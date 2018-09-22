'''
Created on 04/06/2018

@author: marcos
'''
from unicodedata import normalize
import psycopg2

conexao = psycopg2.connect("host=localhost port=5432 dbname=ibge user=postgres password=.senha.")

def remove_acentos(texto):
    if type(texto) == unicode:
        nfkd_form = normalize('NFKD', texto)
        ascii = nfkd_form.encode('ASCII', 'ignore')
        return ascii
    else:
        return texto
