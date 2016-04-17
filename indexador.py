import csv

import numpy


def calculate_tf_idf(freqij,maxi,N,nj):
    return freqij/maxi * numpy.math.log(N/nj)



def main():

    # gerando matrix de peso

    terms = []
    documents_csv = []
    documents = []

    with open('out\invert_list.csv') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in spamreader:
            if (len(row[0]) < 3):
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

    i = 0
    for term_appearance in documents_csv:
        for document_number in term_appearance:
            j = documents.index(document_number)
            matrix[i][j] += 1
        i += 1


    print(matrix)


    N = len(documents)




    column_max = []
    j = len(matrix[0]) - 1
    print(j)
    while(j > -1):
        column_max.append(matrix[:, j].max())
        j -= 1

    i = 0
    for row in matrix:
        print(i)
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


    print(matrix)
main()