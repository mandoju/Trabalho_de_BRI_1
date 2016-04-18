
import configparser
from collections import OrderedDict
import csv

import re

import numpy

import pickle

import logging
import time

class MultiOrderedDict(OrderedDict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            self[key].extend(value)
        else:
            super(OrderedDict,self).__setitem__(key, value)

def special_match(strg, search=re.compile(r'[^A-Z]').search):
    return not bool(search(strg))


def calculate_tf_idf(freqij,maxi,N,nj):
    return freqij/maxi * numpy.math.log(N/nj)


class indexer:

    def __init__(self,terms,documents,matrix):
        self.terms = terms
        self.documents = documents
        self.matrix = matrix

def main():






    logging.info("Program started!")
    terms = []
    documents_csv = []
    documents = []

    # lendo o arquivo com os leia e saida
    config = configparser.RawConfigParser(strict=False, dict_type=MultiOrderedDict)
    logging.info("Reading INDEX.CFG")

    config.read(['INDEX.CFG'])
    entrada = config.get("DEFAULT", "LEIA")
    saida = config.get("DEFAULT", "ESCREVE")


    logging.info ("Reading " + entrada[0])

    begin_time = time.perf_counter()

    with open(entrada[0]) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if (len(row[0]) < 3 and special_match(row[0])):
                continue
            terms.append(row[0])
            text = eval('[' + row[1] + ']')
            documents_csv.append(text[0])

    for row in documents_csv:
        for number in row:
            if(number not in documents):
                documents.append(number)


    matrix = numpy.zeros((len(terms),len(documents)))
    normalized_matrix = numpy.zeros(((len(terms),max(documents) + 1)))
    len(matrix)


    logging.info ("making weight matrix")

    i = 0
    for term_appearance in documents_csv:
        for document_number in term_appearance:
            j = documents.index(document_number)
            matrix[i][j] += 1
        i += 1

    N = len(documents)




    logging.info ("calculating td-idf.")

    column_max = []
    j = len(matrix[0]) - 1
    while(j > -1):
        column_max.append(matrix[:, j].max())
        j -= 1

    i = 0
    for row in matrix:
        j=0

        nj = 0
        for column in row:
            if(column > 0):
                nj += 1

        for column in row:
            freqij = column

            maxi = column_max[j]
            if(freqij > 0):
                matrix[i][j] = calculate_tf_idf(freqij,maxi,N,nj)
            j += 1
        i+= 1

    index = indexer(terms,documents,matrix)

    end_time = time.perf_counter()
    total_time = end_time - begin_time

    logging.info("total index time " + str(total_time) + " for " + str(len(terms)) + " terms and " + str(len(documents)) + " documents" )
    logging.info("indexer made  " + str(len(terms) / total_time) + " terms per second")
    logging.info("indexer made  " + str( len(documents) /total_time) + " documents per second" )



    logging.info("writing on pickle file")
    with open(saida[0],'wb') as output:
        pickle.dump(index,output,pickle.HIGHEST_PROTOCOL)

    logging.info("Finished!")

logging.basicConfig(filename='log\indexador.log', level=logging.INFO,
                    format='%(asctime)s\t%(levelname)s\t%(message)s')
main()