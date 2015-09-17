#!/usr/local/bin/python
################################################################################
#   Prepares raw data for processing by runEPH.py                              #
#   Copyright (C) 2015 Mark Dennehy                                            #
#                                                                              #
#   This program is free software; you can redistribute it and/or modify       #
#   it under the terms of the GNU General Public License as published by       #
#   the Free Software Foundation; either version 2 of the License, or          #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU General Public License for more details.                               #
#                                                                              #
#   You should have received a copy of the GNU General Public License along    #
#   with this program; if not, write to the Free Software Foundation, Inc.,    #
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.                #
################################################################################

import sys
import string
import json
import csv
import numpy
from fuzzywuzzy import fuzz
import editdistance

def apCluster(similarityMatrix):
    responsibilityMatrix = numpy.matrix(numpy.zeros((numOfWorks,numOfWorks)))
    availabilityMatrix = numpy.matrix(numpy.zeros((numOfWorks,numOfWorks)))
    evidenceMatrix = numpy.matrix(numpy.zeros((numOfWorks,numOfWorks)))
    dampingFactor = 0.9
    stableCount = 0

    # Remove degeneracies
    similarityMatrix = similarityMatrix + 1e-12*numpy.random.standard_normal((numOfWorks,numOfWorks))*(numpy.amax(similarityMatrix)-numpy.amin(similarityMatrix));

    maxSimilarities = numpy.amax(similarityMatrix, axis=1)
    precalcResponsibilityDiagonal = numpy.zeros((numOfWorks))
    for i in range(0, numOfWorks):
        precalcResponsibilityDiagonal[i] = similarityMatrix[i,i] - maxSimilarities[i]

    iterations = 0
    # for iterations in range(0, 100):
    while (stableCount < 10) and (iterations < 2000):
        #sys.stdout.write('.')
        #sys.stdout.flush()
        # compute responbilities
        oldResponsibilityMatrix = numpy.copy(responsibilityMatrix)
        tmpMatrix = availabilityMatrix + similarityMatrix

        # find largest element in each row and its location
        tmpMax = numpy.amax(tmpMatrix, axis=1)
        tmpMaxIndices = numpy.argmax(tmpMatrix, axis=1)

        # find second-largest element in each row and its location
        for i in range(0, numOfWorks):
            tmpMatrix[i,tmpMaxIndices[i]] = numpy.finfo(tmpMatrix.dtype).min

        tmpMax2 = numpy.amax(tmpMatrix, axis=1)
        tmpMax2Indices = numpy.argmax(tmpMatrix, axis=1)

        # R(i,k) = S(i,k) - max(A(i,k) + S(i,k))
        responsibilityMatrix = similarityMatrix - numpy.tile(tmpMax,(1,numOfWorks))
        # but for all the R(i,k) where the maximum A+S element *is* element i,k
        # R(i,k) = S(i,k) - nextLargestMaximum(A(i,k) + S(i,k))
        for i in range(0, numOfWorks):
            responsibilityMatrix[i,tmpMaxIndices[i]] = similarityMatrix[i,tmpMaxIndices[i]] - tmpMax2[i]
            responsibilityMatrix[i,i] = precalcResponsibilityDiagonal[i]


        # dampen responsibilities
        responsibilityMatrix = ((1-dampingFactor) * responsibilityMatrix) + (dampingFactor * oldResponsibilityMatrix)

        # compute availabilities
        oldAvailabilityMatrix = availabilityMatrix

        tmpMatrix = numpy.maximum(responsibilityMatrix,0)
        for i in range(0, numOfWorks):
            tmpMatrix[i,i]=responsibilityMatrix[i,i]

        # A(i,k) = min(0, r(k,k)+sum_j!=i(max(0,r(j,k))))
        # A(k,k) = sum_j!=i(max(0,r(j,k)))

        availabilityMatrix = numpy.tile(tmpMatrix.sum(axis=0),(numOfWorks,1)) - tmpMatrix
        availabilityDiagonal = availabilityMatrix.diagonal(offset=0)
        availabilityMatrix = numpy.minimum(availabilityMatrix,0)

        for i in range(0, numOfWorks):
            availabilityMatrix[i,i] = availabilityDiagonal[0,i]

        #  dampen availabilities
        availabilityMatrix = ((1-dampingFactor) * availabilityMatrix) + (dampingFactor * oldAvailabilityMatrix)

        oldEvidenceMatrix = evidenceMatrix
        evidenceMatrix = responsibilityMatrix + availabilityMatrix

        if numpy.array_equal(oldEvidenceMatrix, evidenceMatrix):
            stableCount += 1
        else:
            stableCount = 0

        iterations += 1

    evidenceDiagonal = evidenceMatrix.diagonal(offset=0)
    exemplars = numpy.nonzero(evidenceDiagonal > 0)[1]
    totalDetectedExemplars = numpy.size(exemplars,axis=1)
    exemplarAssignments = numpy.argmax(evidenceMatrix, axis=1)

    uniqueExemplars= set([])
    for i in exemplars:
        uniqueExemplars.add(i)
    print uniqueExemplars

    return totalDetectedExemplars,exemplarAssignments


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: prepareData.py filename.txt\n"
        exit(1)

    nominations = []
    datafile = sys.argv[1]

    # 1984 Hugo Ballot data format
    # "voter","cat","postdate","gotdate","title","numvotes","author","publisher"
    headers=['voter','cat','postdate','gotdate','title','numvotes','author','publisher']

    # 1984 Hugo Ballot categories

    categories=['Best Novel',
                'Best Novella',
                'Best Novelette',
                'Best Short Story',
                'Best Related Work',
                'Best Dramatic Presentation',
                'Best Professional Editor',
                'Best Professional Artist',
                'Best Semiprozine',
                'Best Fanzine',
                'Best Fan Writer',
                'Best Fan Artist',
                'Campbell Award']

#      categories=['Best Novel',
#                  'Best Novella',
#                  'Best Novelette',
#                  'Best Short Story',
#                  'Best Related Work',
#                  'Best Graphic Story',
#                  'Best Dramatic Presentation, Long Form',
#                  'Best Dramatic Presentation, Short Form',
#                  'Best Semiprozine',
#                  'Best Fanzine',
#                  'Best Professional Editor, Long Form',
#                  'Best Professional Editor, Short Form',
#                  'Best Professional Artist',
#                  'Best Fan Writer',
#                  'Best Fan Artist',
#                  'Best Fancast',
#                  'Campbell Award']

    with open(datafile,'rU') as csvfile:
        reader=csv.DictReader(csvfile,headers)
        for row in reader:
            nominations.append({
                'voter'      : row['voter'],
                'preference' : row['numvotes'],
                'title'      : row['title'],
                'author'     : row['author'],
                'publisher'  : row['publisher'],
                'category'   : row['cat'],
                'postdate'   : row['postdate'],
                'gotdate'    : row['gotdate']
            })

    output_works = {}
    output_categories = {}
    output_ballots = {}

    c = 0
    for category in categories:
        c += 1
        output_categories[c] = category

        titles = []
        for nomination in (x for x in nominations if int(x['category']) == c):
            titles.append(nomination['title'])

        numOfWorks = len(titles)
        similarityMatrix = numpy.matrix(numpy.zeros((numOfWorks,numOfWorks)))

        i = 0
        j = 0
        for title in titles:
            for title2 in titles:
                #similarityMatrix[i,j] = fuzz.ratio(title,title2)
                similarityMatrix[i,j] = editdistance.eval(title,title2)
                j += 1
            i += 1
            j = 0

        similarityMatrix /= -100

        numberOfExemplars, exemplarIndices = apCluster(similarityMatrix)

        print exemplarIndices
        i = 0
        for title in titles:
            print title + ' => ' + titles[exemplarIndices[i][0]]
            i+=1


    #with open('data.json','w') as jsonfile:
    #    json.dump(nominations, jsonfile)
