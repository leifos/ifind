#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   04/07/2013
Version: 0.1

Requires:
---------
"""
#TODO(mtbvc): if game_model_functions gets refactored a bit this
#can be made nicer, so refactore populate_pages() and other functs.

from ifind.models import game_model_functions
import argparse
import os

#fetch data for population from file
def get_trending_queries(filename):
    """Extract population data from a file.
       Returns a list of tuples created from comma separated values in file
    """
    f = open(filename, 'r')
    trend_tuples_list = []
    for line in f:
        trend_tuples_list.append(tuple((line.strip()).split(',')))
    f.close()
    return trend_tuples_list

#########
def add_achievements():
    pass

def add_levels():
    pass

#add people... put these functions in another file?

def main():

    parser = argparse.ArgumentParser(
        description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=int,default=True,
                        help="if set to false deletes category from database\
                        if already present.")
    #TODO(mtbvc):won't need this
    parser.add_argument("-cn", "--category_name", type=str,
                        help="Name of category.")
    parser.add_argument("-f", "--filename",
                        default= os.getcwd() + '/data/game_data.txt', type=str,
                        help="relative path to population data file")

    args = parser.parse_args()
    if args.filename:
        data_list = get_trending_queries(args.filename)
        for data_tuple in data_list:
            cat=game_model_functions.get_category(data_tuple[0],append=args.append)
            #data_tuple[1] is url
            game_model_functions.populate_pages([data_tuple[1]],cat)
        return 0
    else:
        print parser.print_help()
        return 2
        #import doctest
        #test_results = doctest.testmod()
        #print test_results
        #if not test_results.failed:
        #    populate(args.file_name, args.category_name, args.append)
        #    print "Category and pages have been populated"
        #return 0


if __name__ == '__main__':
    main()
