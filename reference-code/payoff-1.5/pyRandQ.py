#Simple script for generating random queries
#Author: Sean Galbraith
#Last updated 11/03/13

import random
import math

def randomise(fi, qam, qlen, rup, rlow):
    f = open(fi, "w")
    max_gain = 3
    ideal_query =[max_gain]*qam
    idcg = dcg(ideal_query)

    RANGEUP = rup
    RANGELOW = rlow
    valid = 0
    validq = []
    while valid < qam:
        query = []
        forq = 0
        while forq < qlen:
            query += [random.randint(0,max_gain)]
            forq += 1
        test = dcg(query) / idcg
        if test > rlow and test < rup:
            query += [test]
            validq += [query]
            valid += 1
    for x in validq:
        for y in x:
            f.write(str(y))
        f.write("\n")
    f.close()

def meanap(query):
    total_rel = 30.0
    rank = 0.0
    num_rels = 0.0
    sum_prec = 0.0
    for x in query:
        rank += 1.0
        if int(x) == 1:
            num_rels += 1.0
            cur = num_rels / rank
            sum_prec += cur
    avg_prec = sum_prec / total_rel
    print avg_prec, query
    return avg_prec


def dcg(query):
    rank = 0
    sum_gain = 0.0
    for x in query:
        rank += 1
        if rank == 1:
            sum_gain = float(x)
        else:
            sum_gain += float(x) / math.log(rank,2) 

    print sum_gain, query
    return sum_gain




randomise("randq.txt",10,10,0.5,0.4)
