import sys
import os



from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh import scoring

import operator    


def createScoreFunction(s):
    if (s == 1):
        w = scoring.BM25F(B=0.75, K1=1.5)
        #print "BM25"
    else:
        if (s == 2):
            w = scoring.PL2(c=10.0)
            #print "PL2"
        else:
           w = scoring.BM25F(B=0.75, K1=1.5) 
           #print "BM25"
    return w


work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'test100index')



query_file = "all.new.queries"
result_file = "res.tmp.test"
max_results = 10

#print "Opening Index: " +  my_whoosh_doc_index_dir
ix = open_dir( my_whoosh_doc_index_dir )
ixr = ix.reader()



#qp = MultifieldParser(["title", "content"], schema=ix.schema, group=qparser.OrGroup)
#qp = qparser.QueryParser("content", schema=ix.schema, group=qparser.AndGroup)
#qp = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
qp = qparser.QueryParser("alltext", schema=ix.schema)

sf = createScoreFunction( 1 )
searcher = ix.searcher( weighting=sf )



infile = open(query_file,"r")
outfile = open(result_file,"w")
while infile:
    line = infile.readline()
    parts = line.partition(' ')
            
    query_num = parts[0]
    query_str = unicode( parts[2] )
    max_limit = max_results
    whoosh_query =  qp.parse(query_str)

    results = searcher.search(whoosh_query, limit=max_results)
    n = len(results)
    if n > max_results:
        n = max_results


    for i in range(0, n):
        trec_line = query_num + " Q0 " + str(results[i]['docid']) + " " + str(results[i].rank+1) + " " + str(results[i].score)+"\n"
        trec_line = str(results[i]['docid'])+"\n"
        #print trec_line
        outfile.write(trec_line)
    print query_num, whoosh_query, len(results), n


    if not line:
        break