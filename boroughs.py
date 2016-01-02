#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Week 13 module"""

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
    """This function creates grading scale as a dictionary with float values.

    This function takes exactly one argument, a string which represents the
    filename whose data will be read and interpreted.

    Args:
        file(mix): csv file.

    Returns:
        Returns Value.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
    """
    fhandler = open(filename, 'r')
    files = csv.reader(fhandler)
    data = {}

    for row in files:
        if row[10] not in ['P', '', 'GRADE']:
            data[row[0]] = [row[1], row[10]]
            data.update(data)
    fhandler.close()

    data1 = {}
    for value in data.itervalues():
        if value[0] not in data1.iterkeys():
            value1 = 1
            value2 = GRADES[value[1]]
        else:
            value1 = data1[value[0]][0] + 1
            value2 = data1[value[0]][1] + GRADES[value[1]]
        data1[value[0]] = (value1, value2)
        data1.update(data1)

    retdata = {}
    for key in data1.iterkeys():
        value1 = data1[key][0]
        value2 = data1[key][1]/data1[key][0]
        retdata[key] = (value1, value2)
    return retdata


def get_market_density(filename):
    """This function loads data.

    Args:
        filename(str): some values.

    Return:
        return values.

    Examples:
        >>>get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
    """
    load_file = open(filename, 'r')
    load_data = json.load(load_file)
    ret_data = {}

    for values in load_data['data']:
        place = values[8].strip()

        if place in ret_data:
            ret_data[place] += 1
        else:
            ret_data[place] = 1
    return ret_data


def correlate_data(arg1='inspection_results.csv',
                   arg2='green_markets.json',
                   arg3='result.json'):
    """This function has three arguments that combine data and return average.

    Args:
        arg1(file): csv file.
        arg2(file): contains jason file.
        arg3(file): a file.

    Return:
        returns dict data.

    Example:
        {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """
    output = {}
    avg_score = get_score_summary(arg1)
    avg_data = get_market_density(arg2)
    for key1 in avg_data.iterkeys():
        for key2 in avg_score.iterkeys():
            if key2 == str(key1).upper():
                val1 = avg_score[key2][1]
                val2 = float(avg_data[key1])/(avg_score[key2][0])
                output[key1] = (val1, val2)
                output.update(output)
    jdata = json.dumps(output)
    fhandler = open(arg3, 'w')
    fhandler.write(jdata)
    fhandler.close()
