#!/usr/local/bin/python
################################################################################
#   Runs the E Pluribus Hugo algorithim on the given dataset                   #
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
        print "Usage: runEPH.py filename.json\n"
        exit(1)

    nominations = []
    datafile = sys.argv[1]

    with open(datafile) as data_file:
        nominations = json.load(data_file)

    print len(nominations)

    for nomination in nominations:
        print nomination
        exit

