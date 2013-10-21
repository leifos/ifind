#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   03/07/2013
Version: 0.1

Requires:
---------
"""
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
import random
import argparse

API_KEY = 'bZZNAfF4y5xtIaa6OK/raMdhx4otEVUgBR9acT/fvbc'

def get_trending_queries(filename):
    """Extract trends from a file."""
    f = open(filename, 'r')
    trend_tuples_list = []
    for line in f:
        trend_tuples_list.append(tuple((line.strip()).split(',')))
    f.close()
    return trend_tuples_list

def select_ranks(num_of_ranks, step):
    #TODO make this not stupid
    nums = []
    i=0
    top_range = (0,step)
    while i < (num_of_ranks-1):
        nums.append(random.randrange(top_range[0], top_range[1]))
        if i == 1:
            top_range= (10,20)
        if i == 3:
            top_range = (20,30)
        i+=1
    return nums

def fetch_results(queries_list):
    """Builds a list of tuples (category,url,rank) and returns it """
    myengine = EngineFactory('bing',api_key=API_KEY)
    result_list =[]
    for term in queries_list:
        query = Query(term[1], top=30)
        response = myengine.search(query)
        #TODO implement select_ranks properly maybe (num_to_select,step)
        rank_list = select_ranks(6,10) #TODO make this arguments
        for rank in rank_list:
            #term[0] is trend categoty, term[1] is search term
            try:
                result_list.append((term[0], response.results[rank].url, rank))
                #print "appended" + term[0] + response.results[rank].url
            except IndexError:
                print "index error.."

    print result_list[:]
    return result_list




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', type=str, default='data/trends.txt',
                        help='path to source file for trend data')
    parser.add_argument('-d', '--destination', type=str,
                        help='path to destination file for returned results.')
    args = parser.parse_args()

    if not args.destination:
        parser.print_help()
        return 2
    else:
        trends_list = get_trending_queries(args.source)
        results_list =  fetch_results(trends_list)
        destination_file = open(args.destination, 'a')
        for result in results_list:
            #TODO(mtbvc): use string.format()
            destination_file.write(str(result[0]) + "," + str(result[1]) + "," + str(result[2]) + "\n")


if __name__ == '__main__':
    main()



