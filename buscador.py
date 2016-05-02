import configparser
from collections import OrderedDict
import csv

import re

import numpy

import pickle

import logging
import time

from scipy import spatial

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)


class indexer:

    def __init__(self,terms,documents,matrix):
        self.terms = terms
        self.documents = documents
        self.matrix = matrix

class queryNumber_queryText:
    def __init__(self,queryNumber,queryText):
        self.queryNumber = queryNumber
        self.queryText = queryText

class document_similarity:
    def __init__(self, document, similarity):
        self.document = document
        self.similarity = similarity

    def add_ranking(self,ranking):
        self.ranking = ranking

class query_result:
    def __init__(self,queryNumber,results):
        self.queryNumber = queryNumber
        self.results = results

def main():


    logging.info("Program started!")


    querys = []
    querys_results = []

    # lendo o arquivo com os leia e saida
    config = configparser.RawConfigParser(strict=False, dict_type=MultiOrderedDict)

    logging.info("Reading PC.CFG")


    config.read(['BUSCA.CFG'])
    modelo = config.get("DEFAULT", "MODELO")
    consulta = config.get("DEFAULT", "CONSULTAS")
    resultado = config.get("DEFAULT","RESULTADOS")


    begin_time = time.perf_counter()

    logging.info("Reading model " + str(modelo[0]))


    #carregando o modelo
    with open(modelo[0], "rb") as input_file:
        indexer = pickle.load(input_file)


    logging.info("Reading consults " + str(consulta[0]))

    #carregando consultas
    with open(consulta[0]) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            querys.append(queryNumber_queryText(row[0],row[1]))


    logging.info("Calculating distance")

    # fazendo o calcula da similaridade
    for query in querys:
        #print("making query number" + str(query.queryNumber))
        text = query.queryText
        text = text.split()

        search_vector = numpy.zeros([len(indexer.terms)])
        for word in text:
            if word in indexer.terms:
                search_vector[indexer.terms.index(word)] = 1

        results = []

        i=0
        for column in indexer.matrix.T:
            results.append( document_similarity( indexer.documents[i] ,(spatial.distance.cosine(search_vector, column)) ) )
            i += 1


        results.sort(key=lambda x: x.similarity, reverse=False)

        i=0
        for result in results:
            if(result.similarity < 1):
                result.add_ranking(i)
            else:
                result.add_ranking(-1)
            i+= 1
        a = query_result(query.queryNumber,results)
        querys_results.append(a)

    end_time = time.perf_counter()
    total_time = end_time - begin_time

    logging.info("search made " + str(len(querys_results) / total_time) + " querys per second")


    logging.info("writing on csv")

    with open(resultado[0], 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';',
            quotechar='|', quoting=csv.QUOTE_MINIMAL)

        for result in  querys_results :

            pares_ordernados = '['

            for result_from_query in result.results:
                if(result_from_query.ranking != -1):
                    pares_ordernados += "(" + str(result_from_query.ranking) + "," + str(result_from_query.document) +"," + str(result_from_query.similarity )+ "), "

            pares_ordernados = pares_ordernados[:-2]
            pares_ordernados += ']'
            spamwriter.writerow([result.queryNumber,  pares_ordernados ])
    logging.info("Finished!")


logging.basicConfig(filename='log\\buscador.log', level=logging.INFO,
                    format='%(asctime)s\t%(levelname)s\t%(message)s')
main()