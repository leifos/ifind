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

API_KEY = 'bZZNAfF4y5xtIaa6OK/raMdhx4otEVUgBR9acT/fvbc'

def get_trending_queries(filename):
    f = open(filename, 'r')
    trend_tuples_list = []
    for line in f:
        trend_tuples_list.append(tuple((line.strip()).split(',')))
    f.close()
    return trend_tuples_list

def select_ranks():
    nums = []
    i=0
    top_range = (0,10)
    while i < 5:
        nums.append(random.randrange(top_range[0], top_range[1]))
        if i == 1:
            top_range= (10,20)
        if i == 3:
            top_range = (20,30)
        i+=1
    return nums

def fetch_results(queries_list):
    myengine = EngineFactory('bing',api_key=API_KEY)
    for term in queries_list:
        query = Query(term[1], result_type="Web", format='JSON', top=30)
        response = myengine.search(query)
        #for result in response.results:
        rank_list = select_ranks()
        result_list =[]
        for rank in rank_list:
            print (term[0], response.results[rank].url, rank)
            result_list.append((term[0], response.results[rank].url, rank))
    return result_list



    #pass (cat,query)
    #get result back put into a list + rank
    #select rand 2 from top 10, 10-20, 20-30
    #return list (cat,urls,rank)


l = get_trending_queries('/Users/m/projects/ifind/applications/pagefetch_project/data/trends_20130207.txt')
print fetch_results(l)



