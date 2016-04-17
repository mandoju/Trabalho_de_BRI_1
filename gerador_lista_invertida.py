import configparser
from collections import OrderedDict

from lxml import etree as ET
from xml.dom import minidom
import codecs


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


    #iniciando array de palavras vs documents

    words_documents = []

    #lendo o arquivo com os leia e saida
    config = configparser.RawConfigParser(strict=False,dict_type=MultiOrderedDict)
    config.read(['GLI.CFG'])
    entradas = config.get("DEFAULT","LEIA");
    saida = config.get("DEFAULT", "ESCREVE");

    # parte de ler o xml usando o dtd
    f = codecs.open('db\cfc-2.dtd')
    dtd = ET.DTD(f)

    for entrada in entradas:
        print("printando a entrada " + entrada)
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
            print(dtd.error_log.filter_from_errors())

    with open(saida[0], 'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for wd in words_documents:
            spamwriter.writerow([wd.word,wd.documents])

ler_arquivo_clg()

