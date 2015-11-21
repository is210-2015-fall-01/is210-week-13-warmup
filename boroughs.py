#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Working with a CSV file"""


import json

GRADES = {
    'A': 1.0,
    'B': 0.9,
    'C': 0.8,
    'D': 0.7,
    'F': 0.6
}


def get_score_summary(file_name):
    """Returns BORO average score.

    Args:
        One argument called file_name

    Returns:
        A dictionary,
        containing key: BORO name(string), with a tuple of 2 values;
        total(int) and average(float)

    Example:
        >>>{'BRONX': (156, 0.9762820512820514)...}
    """
    dedup_dict = {}

    i = 0
    csv_f = open(file_name, 'r')
    for line in csv_f:
        if i > 0:
            line_list = []
            line_list = line.split(',')
            if not (line_list[10] in ['P', '']):
                boro_grade_tuple = (line_list[1], line_list[10])
                dedup_dict[line_list[0]] = boro_grade_tuple
        i = i + 1

    csv_f.close()

    bronx_count = 0
    bronx_sum = 0
    queens_count = 0
    queens_sum = 0
    brooklyn_count = 0
    brooklyn_sum = 0
    staten_count = 0
    staten_sum = 0
    manhattan_count = 0
    manhattan_sum = 0
    dedup_keys_list = list(dedup_dict.keys())
    for index_var in dedup_keys_list:
        boro_grade_tuple = dedup_dict[index_var]
        boro = boro_grade_tuple[0]
        grade = GRADES[boro_grade_tuple[1]]
        if boro.upper() == 'QUEENS':
            queens_count = queens_count + 1
            queens_sum = queens_sum + grade
        elif boro.upper() == 'BROOKLYN':
            brooklyn_count = brooklyn_count + 1
            brooklyn_sum = brooklyn_sum + grade
        elif boro.upper() == 'BRONX':
            bronx_count = bronx_count + 1
            bronx_sum = bronx_sum + grade
        elif boro.upper() == 'MANHATTAN':
            manhattan_count = manhattan_count + 1
            manhattan_sum = manhattan_sum + grade
        elif boro.upper() == 'STATEN ISLAND':
            staten_count = staten_count + 1
            staten_sum = staten_sum + grade
    results_dict = {}
    results_dict['BRONX'] = (bronx_count, bronx_sum / bronx_count)
    results_dict['QUEENS'] = (queens_count, queens_sum / queens_count)
    results_dict['BROOKLYN'] = (brooklyn_count, brooklyn_sum / brooklyn_count)
    results_dict['STATEN ISLAND'] = (staten_count, staten_sum / staten_count)
    results_dict['MANHATTAN'] = (manhattan_count, manhattan_sum /
                                 manhattan_count)
    return results_dict


def get_market_density(file_name):
    """Returns a dictionary of the number of green markets per BORO

    Args:
        Takes one argument, file_name

    Attributes:
        csv_f = opens the file
        file_dict = loads the json file
        data_list = A list

    Returns:
        A dictionary with key as BORO names(string) and value as total(int)

    Example:
        >>>{'STATEN ISLAND: 2, ...}
    """

    csv_f = open(file_name, 'r')
    file_dict = json.load(csv_f)
    csv_f.close()

    data_list = file_dict['data']

    bronx_count = 0
    queens_count = 0
    brooklyn_count = 0
    staten_count = 0
    manhattan_count = 0
    for index_var in data_list:
        boro = index_var[8]
        if boro.rstrip().upper() == 'QUEENS':
            queens_count = queens_count + 1
        elif boro.rstrip().upper() == 'BROOKLYN':
            brooklyn_count = brooklyn_count + 1
        elif boro.rstrip().upper() == 'BRONX':
            bronx_count = bronx_count + 1
        elif boro.rstrip().upper() == 'MANHATTAN':
            manhattan_count = manhattan_count + 1
        elif boro.rstrip().upper() == 'STATEN ISLAND':
            staten_count = staten_count + 1
    results_dict = {}
    results_dict['BRONX'] = bronx_count
    results_dict['QUEENS'] = queens_count
    results_dict['BROOKLYN'] = brooklyn_count
    results_dict['STATEN ISLAND'] = staten_count
    results_dict['MANHATTAN'] = manhattan_count
    return results_dict


def correlate_data(rest_score_fn, green_market_fn, output_fn):
    """Combines the two previous datasets

    Args:
       rest_score_fn(mixed)takes data from first function
       green_matket_fn(mixed)takes data from second function
       output_fn(mixed)combines data

    Attributes:
        s_summary(mixed)
        market_dens(mixed)

    Returns:
        A dictionary of tuple

    Example:
        >>>{'BRONX': (0.9762820512820514, 0.1987179487179487}

    """
    s_summary = get_score_summary(rest_score_fn)
    market_dens = get_market_density(green_market_fn)
    results_dict = {}
    dens = market_dens['BRONX'] / float(s_summary['BRONX'][0])
    results_dict['BRONX'] = (s_summary['BRONX'][1], dens)

    dens = market_dens['QUEENS']/ float(s_summary['QUEENS'][0])
    results_dict['QUEENS'] = (s_summary['QUEENS'][1], dens)

    dens = market_dens['BROOKLYN']/ float(s_summary['BROOKLYN'][0])
    results_dict['BROOKLYN'] = (s_summary['BROOKLYN'][1], dens)

    dens = market_dens['MANHATTAN']/ float(s_summary['MANHATTAN'][0])
    results_dict['MANHATTAN'] = (s_summary['MANHATTAN'][1], dens)

    dens = market_dens['STATEN ISLAND']/ float(s_summary['STATEN ISLAND'][0])
    results_dict['STATEN ISLAND'] = (s_summary['STATEN ISLAND'][1], dens)

    fhandler = open(output_fn, 'w')
    json.dump(results_dict, fhandler)
    fhandler.close()
