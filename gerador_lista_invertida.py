import configparser
from collections import OrderedDict

from lxml import etree as ET
from xml.dom import minidom
import codecs


import logging
import time

import unidecode
import re
import csv

#classe para ler  múltiplos "LEIA" do arquivo de configuração
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)


class word_document:
    def __init__(self,word):
         self.word = word
         self.documents = []

    def add_document(self,document):
        self.documents.append(document)

def remover_acentos(txt):
    return unidecode.unidecode(txt)

def ler_arquivo_clg():



    logging.info("Program started!")
    #iniciando array de palavras vs documents

    words_documents = []

    #lendo o arquivo com os leia e saida
    config = configparser.RawConfigParser(strict=False,dict_type=MultiOrderedDict)
    logging.info("Reading GLI.CFG")
    config.read(['GLI.CFG'])
    entradas = config.get("DEFAULT","LEIA");
    saida = config.get("DEFAULT", "ESCREVE");

    logging.info("GLI.CFG has been read")


    logging.info("Reading cfc-2.dtd")

    # parte de ler o xml usando o dtd
    f = codecs.open('db\cfc-2.dtd')
    dtd = ET.DTD(f)

    logging.info("cfc-2.dtd read")



    logging.info("Starting reading xml")

    begin_time = time.perf_counter()
    for entrada in entradas:
        #print("printando a entrada " + entrada)
        logging.info("Reading " + entrada + " xml file")
        root = ET.parse(entrada)
        if(dtd.validate(root)):
            xmldoc = minidom.parse(entrada)
            itemlist = xmldoc.getElementsByTagName('RECORD')
            for s in itemlist:
                recordnum = s.getElementsByTagName('RECORDNUM')
                recordnum =  int(recordnum[0].firstChild.nodeValue)
                abstract = s.getElementsByTagName('ABSTRACT')
                if(len(abstract) > 0):
                    text_to_parse = abstract[0].firstChild.nodeValue
                else:
                    extract = s.getElementsByTagName('EXTRACT')
                    if(len(extract) > 0):
                        text_to_parse = extract[0].firstChild.nodeValue
                    else:
                        continue

                text_to_parse = text_to_parse.upper()
                text_to_parse = re.sub('[^A-Z\ \']+', " ", text_to_parse)
                text_words = text_to_parse.split()

                for word in text_words:
                    word_found = False
                    for wd in words_documents:
                        if(wd.word == word):
                            wd.documents.append(recordnum)
                            word_found = True
                            break
                    if(word_found == False):
                        w = word_document(word)
                        w.documents.append(recordnum)
                        words_documents.append(w)

                #print(s.attributes['RECORDNUM'].value)
        else:
            logging.info(entrada + " xml file didn't pass on dtd validation")

            #print(dtd.error_log.filter_from_errors())

    end_time = time.perf_counter()
    total_time = end_time - begin_time

    logging.info("Inverted list created a list with " + str(len(words_documents)) + " words")
    logging.info("Inverted list made " + str(len(words_documents) / total_time) + " words per second")
    logging.info("Inverted list made " + str(len(entradas) / total_time) + " documents per second")

    logging.info("Writing on csv")

    with open(saida[0], 'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for wd in words_documents:
            spamwriter.writerow([wd.word,wd.documents])
    logging.info("Finished!")


logging.basicConfig(filename='log\gerador_lista_invertida.log', level=logging.INFO,
                    format='%(asctime)s\t%(levelname)s\t%(message)s')
ler_arquivo_clg()

