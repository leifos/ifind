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
    for term in queries_list:
        query = Query(term[1], top=30)
        response = myengine.search(query)
        #TODO implement select_ranks properly maybe (num_to_select,step)
        rank_list = select_ranks(6,10) #TODO make this arguments
        result_list =[]
        for rank in rank_list:
            #term[0] is trend categoty, term[1] is search term
            print (term[0], response.results[rank].url, rank)
            result_list.append((term[0], response.results[rank].url, rank))
    return result_list




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str)
    #args = parser.parse_args()
    #TODO(mtbvc): pass filename, etc as cmd line arguments
    l = get_trending_queries('/Users/m/projects/ifind/applications/pagefetch_project/data/trends_20130207.txt')
    #test
    l2 =  fetch_results(l)
    for el in l2:
        #TODO fix this
        print (el[0] + "," + el[1])


if __name__ == '__main__':
    main()



