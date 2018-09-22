#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on Jul 08, 2018

@author: marcosgeo@yahoo.com
'''
import os
import sys
import time
import traceback

from carregar_limites import carregar_distritos, carregar_municipios
from carregar_enderecos import iniciar as iniciar_enderecos
from carregar_faces import iniciar as iniciar_faces
from limpar_tabelas import limpar_tabelas
from cnefe.municipio import carregar
from utils.conexao import conexao

DISTRITOS =['355030815', '355030816', '355030871']
quadras = False
enderecos = False
limites = False
municipios_arq = r"municipios.shp"
distritos_arq = r"distritos.shp"
pasta = r"ibge/cnefe/shp"


def exibir_menu():
    os.system("clear")
    
    print u"..:: Selecionar uma opção  ::..\n"
    print u"1 - Carregar municipio e distrito"
    print u"2 - Geocodificar lotes"
    print u"3 - Espacializar lotes"
    print u"4 - Classificar atividade dos lotes"
    print u"5 - Espacializar lotes com estimador de intensidade"
    print u"6 - Criar lotes a partir dos endereços"
    print u"7 - Importar limites de municipio e distrito"
    print u"8 - Importar quadras e faces de quadra"
    print u"9 - Importar endereços"
    print u"L - Limpar tabelas"
    print u"X - Sair"
    
    
    return raw_input("\nOpção: ")

def distr_menu():
    print u" -- Selecione o distrito para geocodificar --"
    print u"T - Todos"
    print u"1 - Campo Belo"
    print u"2 - Campo Grande"
    print u"3 - Santo Amaro"
    
    return raw_input("\nOpção: ")


try:
    conex = conexao()
    municipio = None # carregar(conex,'3550308')
    while True:

        opt = exibir_menu()
        msg_voltar_menu = u"\nPressione ENTER para voltar ao menu\n"
    
        if opt.upper() == 'X':
            print u"\nEncerrando"
            break
        elif opt == '1':
            if municipio:
                print u"Municipio carregado"
            else:
                print u"Carregando municipio e lotes"
                municipio = carregar(conex, '3550308')
            raw_input(msg_voltar_menu)
        elif opt == '2':
            if municipio:
                dist_opt = distr_menu()
                if dist_opt == 'T':
                    for dist in municipio.distritos:
                        if dist.codigo in DISTRITOS:
                            dist.geocodificar(conex)
                        print u"\nDistrito geocodificado {}".format(
                            dist)
                    
                elif dist_opt in ['1', '2', '3']:
                    for dist in municipio.distritos:
                        if dist.codigo == DISTRITOS[int(dist_opt)-1]:
                            dist.geocodificar(conex)
                    print u"\nDistrito geocodificado com sucesso"
                else:
                    print u"\nNão existe a opção selecionada"
            else:
                print u"\nMunicípio não carregado"
                
            raw_input(msg_voltar_menu)
        
        elif opt == '4':
            if municipio:
                dist_opt = distr_menu()
                if dist_opt == 'T':
                    for dist in municipio.distritos:
                        if dist.codigo in DISTRITOS:
                            dist.classificar_atividade(conex)
                elif dist_opt in ['1', '2', '3']:
                    for dist in municipio.distritos:
                        if dist.codigo == DISTRITOS[int(dist_opt)-1]:
                            dist.classificar_atividade(conex)
                else:
                    print u'\nNão existe a opção selecionada'
            else:
                print u"\nMunicípio não carregado"
                
            raw_input(msg_voltar_menu)
        
        elif opt == '6':
            print u"Criando lotes do municipio"
            municipio = carregar(conex, '3550308','extrair')
            if municipio:
                print u"Lotes criados com sucesso"
            else:
                print u"Falha ao criar lotes"
            raw_input(msg_voltar_menu)

        elif opt.upper() == 'L':
            e = raw_input(u"\nTem certeza que deseja excluir todos os registros "+\
                      u"das tabelas? ( s / n): ")
            if e.lower() == 's':
                print u"\nExcluindo registros"
                limpar_tabelas()
                quadras = False
                enderecos = False
                limites = False
                municipio = None
                raw_input(msg_voltar_menu)
        elif opt == '7':
            if not limites:
                print u"\nCarregando limites de municipio e distrito"
                carregar_municipios(pasta, municipios_arq)
                carregar_distritos(pasta, distritos_arq)
                limites = True
                raw_input(msg_voltar_menu)
            else:
                print u"\nLimites já carregados."
                time.sleep(5)
        elif opt == '8':
            if not quadras:
                print u"\nCarregando quadras e faces de quadra"
                iniciar_faces()
                quadras = True
                raw_input(msg_voltar_menu)
            else:
                print u"\nQuadras e faces de quadras já carregadas."
                time.sleep(5)
        elif opt == '9':
            if not enderecos:
                print u"\nCarregando endereços"
                iniciar_enderecos()
                enderecos = True
                raw_input(msg_voltar_menu)
            else:
                print u"\nEndereços já carregados."
                time.sleep(5)
except:
    print traceback.format_exc()
finally:
    if conex:
        conex.close()
    
    