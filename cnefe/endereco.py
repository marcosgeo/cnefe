# -*- coding: utf-8 -*-
'''
Created on 03/06/2017

@author: marcosgeo@yahoo.com
'''

class Endereco:
    def __init__(self, endereco):
        
        self.uf = endereco[0:2]
        self.municipio = endereco[0:7]
        self.distrito = endereco[7:9].strip().zfill(2)
        self.subdistrito = endereco[9:11].strip().zfill(2)
        self.setor_cod = endereco[11:15].strip().zfill(4)
        self.setor_sit = endereco[15:16].strip()
        self.lograd_tipo = endereco[16:36].strip()
        self.lograd_titulo = endereco[36:66].strip()
        self.lograd_nome = endereco[66:126].strip()
        self.imovel_numero = int(endereco[126:134])
        self.modificador = endereco[134:141].strip()
        self.elemento1 = endereco[141:161].strip()
        self.valor1 = endereco[161:171].strip()
        self.elemento2 = endereco[171:191].strip()
        self.valor2 = endereco[191:201].strip()
        self.elemento3 = endereco[201:221].strip()
        self.valor3 = endereco[221:231].strip()
        self.elemento4 = endereco[231:251].strip()
        self.valor4 = endereco[251:261].strip()
        self.elemento5 = endereco[261:281].strip()
        self.valor5 = endereco[281:191].strip()
        self.elemento6 = endereco[291:311].strip()
        self.valor6 = endereco[311:321].strip()
        self.latitude = endereco[321:336].strip()
        self.longitude = endereco[336:351].strip()
        self.localidade = endereco[351:411].strip()
        self.especie = endereco[471:473].strip()
        self.nome_estab = endereco[473:513].strip()
        self.indicador = endereco[513:514].strip()
        self.domicilio_coletivo = endereco[514:544].strip()
        self.quadra = endereco[544:547].strip()
        self.face = endereco[547:550].strip()
        self.cep = endereco[550:557].strip().zfill(8)
        self.setor_id = self.municipio + self.distrito + self.subdistrito +\
            self.setor_cod
