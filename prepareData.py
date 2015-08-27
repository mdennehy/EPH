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

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: prepareData.py filename.txt\n"
        exit(1)

    datafile = sys.argv[1]

    # 1984 Hugo Ballot data format
    # "voter","cat","postdate","gotdate","title","numvotes","author","publisher"
    headers=['voter','cat','postdate','gotdate','title','numvotes','author','publisher']

    with open(datafile,'rU') as csvfile:
        reader=csv.DictReader(csvfile,headers)
        for row in reader:
            for h in headers:
                print (h+' '+row[h])


