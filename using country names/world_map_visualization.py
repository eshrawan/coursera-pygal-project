"""
presenting data on a world map using pygal and common two-letter country codes

author: @eshrawan
"""

# importing necessary mosules for project
import csv
import math
import pygal

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Outputs:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    list_tups = list(filter(lambda tup: tup[1] in gdp_countries,   plot_countries.items()))
    finaldict = dict(list_tups)
    list_tups_2 = list(filter(lambda tup: tup[1] not in gdp_countries,  plot_countries.items()))
    finalset = set([item[0] for item in list_tups_2])
    return finaldict, finalset


def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    plot_dict ={}
    plot_dict_1 ={}
    plot_set_1 = set()
    plot_set_2 = set()
    new_data_dict = {}
    with open(gdpinfo['gdpfile'], 'r') as data_file:
        data = csv.DictReader(data_file, delimiter=gdpinfo['separator']
                                      ,quotechar = gdpinfo['quote'])
    for row in data:
        new_data_dict[row[gdpinfo['country_name']]] = row

        plot_dict, plot_set_1 = reconcile_countries_by_name(plot_countries, new_data_dict)

        for key,value in plot_dict.items():
            for key1,val1 in new_data_dict.items():
                if value == key1:
                    if val1[year]!='':
                        plot_dict_1[key] = math.log(float(val1[year]),10)
                    else:
                        plot_set_2.add(key)

    return plot_dict_1, set(plot_set_1), set(plot_set_2)



def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    plot_dict_1, plot_set_1, plot_set_2 = build_map_dict_by_name(gdpinfo, plot_countries, year)
    worldmap = pygal.maps.world.World()
    title_map = 'GDP by country for ' + year + ' (log scale), unifiedby common country NAME'
    worldmap.title = title_map
    label_map = 'GDP for ' + year
    worldmap.add(label_map,plot_dict_1 )
    worldmap.add('Missing from World Bank Data',plot_set_1 )
    worldmap.add('No GDP Data' ,plot_set_2 )
    worldmap.render_in_browser()
