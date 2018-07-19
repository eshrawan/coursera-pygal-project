"""
Project to display GDP data on world map using country codes
author: @eshrawan
"""

import csv
import math
import pygal

#function taken from earlier ocurse project on csv files
# code auhtor: @eshrawan

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, newline='') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
            rowid = row[keyfield]
            table[rowid] = row
    return table

def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary
    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    newtest = read_csv_as_nested_dict(codeinfo['codefile'],
    codeinfo['plot_codes'], codeinfo['separator'], codeinfo['quote'])
    dictionary = {}
    for item in newtest:
        dictionary[item] = newtest[item][codeinfo['data_codes']]
    return dictionary

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data
    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.
      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    valid_countries = {}
    invalid_countries = set()
    lis = build_country_code_converter(codeinfo)
    for items in plot_countries:
        if items.upper() in lis:
            new = lis[items.upper()]
            if new in gdp_countries:
                valid_countries[items] = new
            else:
                invalid_countries.add(items)

        else:
            invalid_countries.add(items)
    return (valid_countries, invalid_countries)

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping
    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    newtest = read_csv_as_nested_dict(gdpinfo['gdpfile'],
    gdpinfo['country_code'], gdpinfo['separator'], gdpinfo['quote'])
    new = reconcile_countries_by_code(codeinfo, plot_countries, newtest)
    valid_countries = {}
    invalid_countries = set()
    zero_set = set()
    lis = build_country_code_converter(codeinfo)

    for items in plot_countries:
        if items.upper() in lis:
            new = lis[items.upper()]
            if new in newtest:
                if newtest[new][year] == '' or newtest[new][year] == 0:
                    zero_set.add(items)
                else:
                    valid_countries[items] = math.log(float(newtest[new][year]), 10)
            else:
                invalid_countries.add(items)
        else:
            invalid_countries.add(items)
    return  (valid_countries , invalid_countries ,  zero_set)
