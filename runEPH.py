#!/usr/local/bin/python
# This Python file uses the following encoding: utf-8
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

def calculationPhase(ballots):
# (1) Calculation Phase: First, the total number of nominations (the number of
# ballots on which each nominee appears) from all eligible ballots shall be
# tallied for each remaining nominee.
    total_number_of_nominations={}

    for ballot in ballots:
        for vote in ballot:
            if vote['work'] not in total_number_of_nominations:
                total_number_of_nominations[vote['work']] = 1
            else:
                total_number_of_nominations[vote['work']] += 1

# Next, a single “point” shall be assigned to each nomination ballot. That
# point shall be divided equally among all remaining nominees on that
# ballot. Finally, all points from all nomination ballots shall be totaled
# for each nominee in that category.

    nominee_points_total={}

    for ballot in ballots:
        points_per_vote = 1.0 / len(ballot)
        for vote in ballot:
            if vote['work'] not in nominee_points_total:
                nominee_points_total[vote['work']] = points_per_vote
            else:
                nominee_points_total[vote['work']] += points_per_vote

#  These two numbers, point total and number of nominations, shall be used
#  in the Selection and Elimination Phases.

    return total_number_of_nominations, nominee_points_total

def selectionPhase(nominee_points_total):
# (2) Selection Phase: The two nominees with the lowest point totals shall be
# selected for comparison in the Elimination Phase. (See 3.A.3 for ties.)

    selection_nominees = sorted(nominee_points_total, key=nominee_points_total.get)
    selected_nominees = []

# 3.A.3: Ties shall be handled as described below:
# (1) During the Selection Phase, if two or more nominees are tied for the
# lowest point total, all such nominees shall be selected for the Elimination
# Phase.
    if selection_nominees[0] == selection_nominees[1]:
        i = 0
        while selection_nominees[i] == selection_nominees[i+1]:
            selected_nominees.append(selection_nominees[i])
            i+=1
        selected_nominees.append(selection_nominees[i])

# (2) During the Selection Phase, if one nominee has the lowest point total and
# two or more nominees are tied for the second-lowest point total, then all such
# nominees shall be selected for the Elimination Phase.
    elif selection_nominees[0] < selection_nominees[1] and selection_nominees[1] == selection_nominees[2]:
        i = 1
        selected_nominees.append(selection_nominees[0])
        while selection_nominees[i] == selection_nominees[i+1]:
            selected_nominees.append(selection_nominees[i])
            i+=1
        selected_nominees.append(selection_nominees[i])

    else:
        selected_nominees = selection_nominees[0:2]

    return selected_nominees

def eliminateWork(work,ballots):
    for ballot in ballots:
        for vote in ballot:
            if vote['work'] == work:
                ballot.remove(vote)

def eliminationPhase(elimination_candidates, total_number_of_nominations, nominee_points_total, ballots, works):
# (3) Elimination Phase: Nominees chosen in the Selection Phase shall be
# compared, and the nominee with the fewest number of nominations shall be
# eliminated and removed from all ballots for the Calculation Phase of all
# subsequent rounds. (See 3.A.3 for ties.)
    candidates = []

    if total_number_of_nominations[elimination_candidates[0]] == total_number_of_nominations[elimination_candidates[1]]:
# 3.A.3: Ties shall be handled as described below:
# (3) During the Elimination Phase, if two or more nominees are tied for the
# fewest number of nominations, the nominee with the lowest point total at that
# round shall be eliminated.

# (4) During the Elimination Phase, if two or more nominees are tied for both
# fewest number of nominations and lowest point total, then all such nominees
# tied at that round shall be eliminated.

        for candidate in elimination_candidates:
            if total_number_of_nominations[elimination_candidates[0]] < total_number_of_nominations[candidate]:
                elimination_candidates.remove(candidate)

        for candidate in elimination_candidates:
            if nominee_points_total[elimination_candidates[0]] < nominee_points_total[candidate]:
                elimination_candidates.remove(candidate)

    else:
        candidates.append(elimination_candidates[0])

    for candidate in candidates:
        eliminateWork(candidate,ballots)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: runEPH.py filename.json\n"
        exit(1)

    datafile = sys.argv[1]

    works = {}
    categories = {}
    ballots = []

    with open(datafile) as data_file:
        data = json.load(data_file)
        for work in data['works']:
            works[work['id']] = work['title']
        for category in data['categories']:
            categories[category['id']] = category['name']
        for ballot in data['ballots']:
            votes = []
            for vote in ballot['votes']:
                votes.append({'work':vote['work'],'preference':vote['preference']})
            ballots.append({'category':ballot['category'], 'votes':votes})

    works_by_category = {}
    for category in iter(categories):
        works_by_category[category] = set([])

    for ballot in ballots:
        for vote in ballot['votes']:
            works_by_category[ballot['category']].add(vote['work'])

    ballots_by_category = {}
    for category in iter(categories):
        ballots_by_category[category] = []

    for ballot in ballots:
        ballots_by_category[ballot['category']].append(ballot['votes'])

    print works_by_category

    print ballots_by_category

    print "Data loaded. Running EPH."

# 3.8.1: Except as provided below, the final Award ballots shall list in each
# category the five eligible nominees receiving the most nominations. If there
# is a tie including fifth place, all the tied eligible nominees shall be
# listed. determined by the process described in section 3.A.
    targetNumberOfFinalists = 5

# Section 3.A: Finalist Selection Process
# 3.A.1: For each category, the finalist selection process shall be conducted as
# elimination rounds consisting of three phases:
    for category in iter(categories):

# 3.A.2: The phases described in 3.A.1 are repeated in order for each category
# until the number of finalists specified in 3.8.1 remain. If elimination would
# reduce the number of finalists to fewer than the number specified in section
# 3.8.1, then instead no nominees will be eliminated during that round, and all
# remaining nominees shall appear on the final ballot, extending it if
# necessary.
        while len(works_by_category[category]) < targetNumberOfFinalists:
            total_number_of_nominations, nominee_points_total = calculationPhase(ballots_by_category[category])
            elimination_candidates = selectionPhase(nominee_points_total)
            eliminationPhase(elimination_candidates, total_number_of_nominations, nominee_points_total, ballots_by_category[category], works_by_category[category])

    print works_by_category
# 3.A.4: After the initial Award ballot is generated, if any finalist(s) are
# removed for any reason, the finalist selection process shall be rerun as
# though the removed finalist(s) had never been nominee(s). None of the
# remaining original finalists who have been notified shall be removed as a
# result of this rerun. The new finalist(s) shall be merged with the original
# finalists, extending the final ballot if necessary.
