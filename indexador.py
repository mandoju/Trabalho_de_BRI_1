import csv

import numpy


def main():

    # gerando matrix de peso

    terms = []
    documents_csv = []
    documents = []

    with open('out\invert_list.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            terms.append(row[0])
            text = eval('[' + row[1] + ']')
            documents_csv.append(text[0])

    for row in documents_csv:
        for number in row:
            if(number not in documents):
                documents.append(number)

    matrix = numpy.zeros((len(terms),max(documents) + 1))
    len(matrix)

    i = 0
    for term_appearance in documents_csv:
        for document_number in term_appearance:
            matrix[i][document_number] += 1
        i += 1

    print(matrix)
main()