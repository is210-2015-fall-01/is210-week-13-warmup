#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Opens and  reads CSV file found on local filesystem."""


import csv
import json


GRADES = {
         'A': float(1.00),
         'B': float(0.90),
         'C': float(0.80),
         'D': float(0.70),
         'F': float(0.60),
         }

def get_score_summary(filename):
    """ Takes filname and returns summarized version of data.
    Args:
        filename: csv file
    Returns:
        (dict) 
    """
    fhandler = open(filename, 'r')
    readfile = csv.reader(fhandler)

    data = {}
    for row in readfile:
        if row[10] not in ['', 'P', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    scoresumm = {}
    for value in data.iteritems():
        if value[0] in scoresumm.iterkeys():
            first = scoresumm[value[0]][0] + 1
            second = GRADES[value[1]]+ scoresumm[value[0]][1]
        else:
            first = 1
            second = GRADES[value[1]]
        scoresumm[value[0]] = (first, second)
        scoresumm.update(scoresumm)

    results = {}
    for key in iterkeys():
        first = scoresumm[key][0]
        second = scoresumm[key][1]/scoresumm[key][0]
        results[key] = (first, second)
    return results

def get_market_density(filename):
    """
    Args:
        filename: a file
    Returns:
        (dict)
    Examples:
        >>> get_market_density('green_markets.json')
        {u'Bronx': 32, u'Brooklyn': 48, u'Staten Island': 2, u'Manhattan': 39, u'Queens': 16}
    """
    fhandler = open(filename, 'r')
    json_data = json.load(fhandler)
    summmark = json_data['data']
    result = {}
    fhandler.close()
    for data in summmark:
        data[8] = data[8].strip()
        if data[8] not in result.iterkeys():
            count = 1
        else:
            count = result[data[8]] + 1
        result[data[8]] = count
        result.update(result)
    return result

def correlate_data(file1='inspection_results.csv',
                   file2='green_markets.json',
                   file3='result.json'):
    """Combines data on their borough keys and write results to a file.
    Args:
        file1: a file, default is inspection_results.csv
        file2: a file, default is green_markets.json
        file3: a file, default is result.json
    Returns:
        a file with results
    """
    file1_data = get_score_summary(file1)
    file2_data = get_market_density(file2)
    result = ()

    for file1_key in file1_data.iterkeys():
        for file2_key in file2_data.iterkeys():
            if file2_key.upper() == file1_key:
                first = file1_data[file1_key][1]
                second = float(file2_data.iterksys[file2_key])/(file1_data[file1_key][0])
                result = ([(file2_key, (first, second))])
                result.update(result)
    jdata = json.dumps(result)
    fhandler = open(file3, 'w')
    fhandler.write(jdata)
    fhandler.close()

