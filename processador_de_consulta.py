import configparser
from collections import OrderedDict
from lxml import etree as ET
from xml.dom import minidom
import codecs
import re
import csv



class querynum_querytext:

    def __init__(self,querynum,querytext):
        self.querynum = querynum
        self.querytext = querytext

class querynum_parlist:

    def __init__(self,querynum):
        self.querynum = querynum
        self.querylist = []

#classe para ler  múltiplos "LEIA" do arquivo de configuração
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)


def main():

    # lendo o arquivo com os leia ,consulta e esperados
    config = configparser.RawConfigParser(strict=False, dict_type=MultiOrderedDict)
    config.read(['PC.CFG'])
    entradas = config.get("DEFAULT", "LEIA");
    consulta = config.get("DEFAULT", "CONSULTAS");
    esperado = config.get("DEFAULT", "ESPERADOS");

    f = codecs.open('db\cfcquery-2.dtd')
    dtd = ET.DTD(f)


    row_consulta = []
    row_esperados = []

    for entrada in entradas:
        root = ET.parse(entrada)
        if (dtd.validate(root)):
            xmldoc = minidom.parse(entrada)
            itemlist = xmldoc.getElementsByTagName('QUERY')
            for s in itemlist:
                querynum = s.getElementsByTagName('QueryNumber')
                querynum = int(querynum[0].firstChild.nodeValue)
                querytextnode = s.getElementsByTagName('QueryText')
                querytext = querytextnode[0].firstChild.nodeValue
                querytext = querytext.upper()
                querytext = re.sub('[^A-Z\ \']+', " ", querytext)
                row_consulta.append(querynum_querytext(querynum,querytext))

                recordlist = s.getElementsByTagName('Records')
                for r in recordlist:
                    itemList = r.getElementsByTagName('Item')
                    for i in itemlist:
                        2+2
                #row_esperados.append(querynum_parlist(querynum,))
        else:
            print(dtd.error_log.filter_from_errors())

    with open(consulta[0], 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in row_consulta:
            spamwriter.writerow([row.querynum,row.querytext])

#    with open(consulta[0], 'w', newline='') as csvfile:
#        spamwriter = csv.writer(csvfile, delimiter=';',
#                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
#        for row in row_esperados:
#            spamwriter.writerow([row.querynum, row.querytext])

main()