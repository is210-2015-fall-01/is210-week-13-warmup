#!/usr/bin/env python
# _*_ coding: utf-8 -*-
"""This is boroughs.py docstring."""

import csv
import json


def get_score_summary(score_file):
    """This funtion summarizes score data.

    Score data is extrated from a csv file and average score is calculated
    for every borough.

    Args:
        file (file): A CSV file containing the score data.

    Returns:
        score summary (dict): A summary of score results for each borough.

    Example:
        >>> get_score_summary('inspection_results.csv')
        >>> {'BRONX': (156, 0.9762820512820514), 'BROOKLYN':
        (417, 0.9745803357314141), 'STATEN ISLAND': (46, 0.9804347826086955),
        'MANHATTAN': (748, 0.9771390374331531), 'QUEENS':
        (414, 0.9719806763285017)}
        """
    mydict = {
        'A': float(1.0),
        'B': float(0.9),
        'C': float(0.8),
        'D': float(0.7),
        'F': float(0.6)
        }
    all_dict = {}
    fhandler = open(score_file, 'r')
    first_line = fhandler.readline()
    if first_line:
        pass
    myfile = csv.reader(fhandler)

    for line in myfile:
        if not line[10] == '' and not line[10] == 'P':
            all_dict[line[0]] = [line[1], line[10]]
            all_dict.update(all_dict)
    fhandler.close()

    sum_dict = {}
    for value in all_dict.iteritems():
        if value[1][0] not in sum_dict.iterkeys():
            boro = value[1][0]
            count = 1
            grade = mydict[value[1][1]]
        else:
            boro = value[1][0]
            count = sum_dict[boro][0] + 1
            grade = sum_dict[boro][1] + mydict[value[1][1]]
        record = dict([(boro, (count, grade))])
        sum_dict.update(record)

    for boro, (count, grade) in sum_dict.iteritems():
        avg = grade / count
        record = dict([(boro, (count, avg))])
        sum_dict.update(record)
    return sum_dict


def get_market_density(market_file):
    """This funtion calculates market share.

    Market share is calculated for every borough.

    Args:
        file (file): A json file containing the market data.

    Returns:
        market density (dict): The number of markets per borough.

    Example:
        >>> get_market_density('green_markets.json')
        {u'STATEN ISLAND': 2, u'BROOKLYN': 48, u'BRONX': 32,
        u'MANHATTAN': 39, u'QUEENS': 16}
        """
    filehandler = open(market_file).read()
    json_data = json.loads(filehandler)
    sum_markets = {}

    for boro in json_data['data']:
        boro[8] = boro[8].strip()
        if boro[8] not in sum_markets.iterkeys():
            count = 1
        else:
            count = sum_markets[boro[8]] + 1
        record = dict([(boro[8], count)])
        sum_markets.update(record)
    return sum_markets


def correlate_data(score_file, market_file, output):
    """This is the correlate_data module;

    This modules correlates data from the score data and the
    market density data.

    Args:
        score_file (file): CSV file containing the score data.
        market_file (file): JSON file containing the market info.
        output (file): Output file where the results are stored:
    Returns:
        Combined info (dict): A dictionary with combined info.

    Example:
        {'BRONX': (0.9762820512820514, 0.1987179487179487)}
    """
    score_data = get_score_summary(score_file)
    market_data = get_market_density(market_file)
    final = {}

    for score_key in score_data.iterkeys():
        for market_key in market_data.iterkeys():
            if market_key.upper() == score_key:
                food_score = score_data[score_key][1]
                market_rest = float(market_data
                                    [market_key])/(score_data[score_key][0])
                record = ([(market_key, (food_score, market_rest))])
                final.update(record)
    json_data = json.dumps(final)
    fhandler = open(output, 'w')
    fhandler.write(json_data)
    fhandler.close()

    return final
