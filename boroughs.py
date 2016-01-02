#!user/bin/env python
# -*- coding: utf-8 -*-
"""Opening Files"""

import csv
import json

GRADES = {
    'A': 1.0,
    'B': .90,
    'C': .80,
    'D': .70,
    'F': .60
}


def get_score_summary(filename):
    """Reads from csv spreadsheet to obtain data on boroughs.
    Args:
        filename(str): filename of csv file
    Returns:
        dictionary showing # of restaurants per borough and avg score
    Examples:
    >>>get_score_summary('inspection_results.csv')
    {'BRONX': (156, 0.9762820512820513),
     'STATEN ISLAND': (46, 0.9804347826086957),
     'BROOKYN': (417, 0.9745803357314149),
     'MANHATTAN': (748, 0.9771390374331551),
     'QUEENS': (414, 0.9719806763285024)}
    """
    csvfile = open(str(filename), 'r')
    readfile = csv.reader(csvfile)
    next(readfile, None)
    new_db = []
    new_keys = []
    for line in readfile:
        db_key = line[0]
        borough = line[1]
        grade = line[10]
        if grade == 'P' or grade == '':
            continue
        grade_score = GRADES[grade]
        new_db.append(db_key)
        new_keys.append((borough, grade_score))
    new_db2 = dict(zip(new_db, new_keys))
    csvfile.close()

    count_man = 0
    count_que = 0
    count_brook = 0
    count_bron = 0
    count_sta = 0
    score_man = 0
    score_que = 0
    score_brook = 0
    score_bron = 0
    score_sta = 0
    for dummy, value in new_db2.iteritems():
        if value[0] == 'MANHATTAN':
            count_man += 1
            score_man += value[1]
            avg_man = (score_man / count_man)
        elif value[0] == 'QUEENS':
            count_que += 1
            score_que += value[1]
            avg_que = (score_que / count_que)
        elif value[0] == 'BROOKLYN':
            count_brook += 1
            score_brook += value[1]
            avg_brook = (score_brook / count_brook)
        elif value[0] == 'BRONX':
            count_bron += 1
            score_bron += value[1]
            avg_bron = (score_bron / count_bron)
        elif value[0] == 'STATEN ISLAND':
            count_sta += 1
            score_sta += value[1]
            avg_sta = (score_sta / count_sta)

    borodict = {
        'MANHATTAN': (count_man, avg_man),
        'QUEENS': (count_que, avg_que),
        'BROOKLYN': (count_brook, avg_brook),
        'BRONX': (count_bron, avg_bron),
        'STATEN ISLAND': (count_sta, avg_sta),
    }

    return borodict


def get_market_density(filename):
    """Retrieve dict from file and shows how many markets per borough.
    Args:
        filename (str): json file to open
    Returns:
        dict of each borough as keys, which value as amount of markets
    Examples:
        >>>get_market_density('green_markets.json')
        {u'Bronx': 32, u'Brooklyn': 48, u'Staten Island': 2,
         u'Manhattan': 39, u'Queens': 16}
    """
    jsonfile = open(str(filename), 'r')
    green_dict = json.load(jsonfile)
    loop_dict = green_dict['data']
    market_dict = {}
    for market in loop_dict:
        boro = market[8].strip()
        if boro not in market_dict:
            market_count = 1
            market_dict[boro] = market_count
        else:
            market_dict[boro] += market_count
    jsonfile.close()
    return market_dict


def correlate_data(csvfile, jsonfile, outputfile='outputfile.txt'):
    """Takes data from files, creates new dict and writes it into new file.
    Args:
        csffile (str)
        jsonfile (str)
        outputfile (str): default = 'outputfile.txt'
    Returns:
        write dict to file
    Examples:
        >>>correlate_data('inspection_results.csv', 'green_markets.json')
    """
    sdict = get_score_summary(csvfile)
    mdict = get_market_density(jsonfile)
    ndict = {}
    for key in sdict.iterkeys():
        for key2 in mdict.iterkeys():
            if key == key2.upper():
                ndict[key] = (sdict[key][1], (mdict[key2]/float(sdict[key][0])))
    fhandler = open(outputfile, 'w')
    json.dump(ndict, fhandler)
    fhandler.close()
