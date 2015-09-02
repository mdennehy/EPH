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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: prepareData.py filename.txt\n"
        exit(1)

    nominations = []
    datafile = sys.argv[1]

    # 1984 Hugo Ballot data format
    # "voter","cat","postdate","gotdate","title","numvotes","author","publisher"
    headers=['voter','cat','postdate','gotdate','title','numvotes','author','publisher']

    with open(datafile,'rU') as csvfile:
        reader=csv.DictReader(csvfile,headers)
        for row in reader:
            nominations.append({
                'voter'      : row['voter'],
                'preference' : row['numvotes'],
                'title'      : row['title'],
                'author'     : row['author'],
                'publisher'  : row['publisher'],
                'cat'        : row['cat'],
                'postdate'   : row['postdate'],
                'gotdate'    : row['gotdate']
            })

    #numOfVotes = len(nominations)
    #similarityMatrix = numpy.matrix(numpy.zeros((numOfVotes,numOfVotes)))


    with open('reference/ToyProblemSimilarities.txt','rU') as sfile:
        sims=csv.DictReader(sfile,fieldnames=['x','y','s'])
        numOfVotes=0
        for row in sims:
            numOfVotes += 1
        sfile.seek(0)
        similarityMatrix = numpy.matrix(numpy.zeros((numOfVotes,numOfVotes)))
        for row in sims:
            similarityMatrix[int(row['x']),int(row['y'])] = float(row['s'])
            similarityMatrix[int(row['y']),int(row['x'])] = float(row['s'])
        for i in range(0, numOfVotes):
            similarityMatrix[i,i]=-15.561256

    print similarityMatrix

    responsibilityMatrix = numpy.matrix(numpy.zeros((numOfVotes,numOfVotes)))
    availabilityMatrix = numpy.matrix(numpy.zeros((numOfVotes,numOfVotes)))
    dampingFactor = 0.9

    # Remove degeneracies
    similarityMatrix = similarityMatrix + 1e-12*numpy.random.standard_normal((numOfVotes,numOfVotes))*(numpy.amax(similarityMatrix)-numpy.amin(similarityMatrix));


    for iterations in range(0, 100):
        # compute responbilities
        oldResponsibilityMatrix = numpy.copy(responsibilityMatrix)
        tmpMatrix = availabilityMatrix + similarityMatrix

        # find largest element in each row and its location
        tmpMax = numpy.amax(tmpMatrix, axis=1)
        tmpMaxIndices = numpy.argmax(tmpMatrix, axis=1)

        # find second-largest element in each row and its location
        for i in range(0, numOfVotes):
            tmpMatrix[i,tmpMaxIndices[i]] = numpy.finfo(tmpMatrix.dtype).min

        tmpMax2 = numpy.amax(tmpMatrix, axis=1)
        tmpMax2Indices = numpy.argmax(tmpMatrix, axis=1)

        # R(i,k) = S(i,k) - max(A(i,k) + S(i,k))
        responsibilityMatrix = similarityMatrix - numpy.tile(tmpMax,(1,numOfVotes))
        # but for all the R(i,k) where the maximum A+S element *is* element i,k
        # R(i,k) = S(i,k) - nextLargestMaximum(A(i,k) + S(i,k))
        for i in range(0, numOfVotes):
            responsibilityMatrix[i,tmpMaxIndices[i]] = similarityMatrix[i,tmpMaxIndices[i]] - tmpMax2[i]

        # dampen responsibilities
        responsibilityMatrix = ((1-dampingFactor) * responsibilityMatrix) + (dampingFactor * oldResponsibilityMatrix)

        # compute availabilities
        oldAvailabilityMatrix = availabilityMatrix

        tmpMatrix = numpy.maximum(responsibilityMatrix,0)
        for i in range(0, numOfVotes):
            tmpMatrix[i,i]=responsibilityMatrix[i,i]

        # A(i,k) = min(0, r(k,k)+sum_j!=i(max(0,r(j,k))))
        # A(k,k) = sum_j!=i(max(0,r(j,k)))

        availabilityMatrix = numpy.tile(tmpMatrix.sum(axis=0),(numOfVotes,1)) - tmpMatrix
        availabilityDiagonal = availabilityMatrix.diagonal(offset=0)
        availabilityMatrix = numpy.minimum(availabilityMatrix,0)

        for i in range(0, numOfVotes):
            availabilityMatrix[i,i] = availabilityDiagonal[0,i]

        #  dampen availabilities
        availabilityMatrix = ((1-dampingFactor) * availabilityMatrix) + (dampingFactor * oldAvailabilityMatrix)

# the combined evidence r(i, k)+a(i, k) is stored in the NxN
# matrix E, the number of exemplars is stored in K, and the indices of the exemplars for the
# data points are stored in the N-vector idx (point i is assigned to the data point with index idx(i).)

    evidenceMatrix = responsibilityMatrix + availabilityMatrix

    evidenceDiagonal = evidenceMatrix.diagonal(offset=0)
    I = numpy.nonzero(evidenceDiagonal > 0)[1]

    K = numpy.size(I,axis=1)

    G = numpy.take(similarityMatrix,I,axis=1)
    tmp = numpy.amax(G,axis=1)
    c = numpy.argmax(G,axis=1)

    print G
    print tmp
    print c
# c(I)=1:K;
    c[0][I] = range(K)
# idx=I(c); % Assignments
    idx=I[c]


