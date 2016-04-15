from collections import OrderedDict
import configparser
from xml.parsers.xmlproc import dtdparser


#classe para ler  múltiplos "LEIA" do arquivo de configuração
class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)



def ler_arquivo_clg():


    #lendo o arquivo com os leia e saida
    config = configparser.RawConfigParser(strict=False,dict_type=MultiOrderedDict)
    config.read(['GLI.cfg'])
    entradas = config.get("DEFAULT","LEIA");
    saida = config.get("DEFAULT", "ESCREVE");
    dtd = dtdparser.load_dtd('db\cfc-2.dtd')


    # parte de ler o xml usando o dtd
    attr_separator = '_'
    child_separator = '_'

    for name, element in dtd.elems.items():
        for attr in element.attrlist:
            output = '%s%s%s = ' % (name, attr_separator, attr)
            print
            output
        for child in element.get_valid_elements(element.get_start_state()):
            output = '%s%s%s = ' % (name, child_separator, child)
            print
            output


ler_arquivo_clg()

