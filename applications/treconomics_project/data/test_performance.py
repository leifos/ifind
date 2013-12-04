__author__ = 'leif'

import os
from ifind.search.engines.whooshtrecnews import WhooshTrecNews
from ifind.search.query import Query

def run_queries(engine, query_file, result_file):
    infile = open(query_file,"r")
    outfile = open(result_file,"w")
    while infile:
        line = infile.readline()
        parts = line.partition(' ')
        query_num = parts[0]
        query_str = unicode( parts[2] )
        max_limit = 1000
        print query_num, query_str

        def buildQueryParts(term_list, op):
            qp = ''
            for t in term_list:
                if t:
                    if qp:
                        qp = qp + " "+ op  +" " + t
                    else:
                        qp = t
            return qp

        #or_query=  buildQueryParts(query_str.split(' '), 'OR')

        #query = Query(terms=or_query,top=1000)
        query = Query(terms=query_str,top=1000)
        query.skip = 1
        response = engine.search(query)

        if response:
            print query_num + " " + str(len(response.results))

            rank = 0
            for r in response.results:
                rank = rank + 1
                trec_line = query_num + " Q0 " + r.docid + " " + str( rank) + " " + str(1000-rank) + " Exp\n"
                outfile.write(trec_line)

        if not line:
            break



work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'fullindex')

query_file = os.path.join(work_dir,'queries.trec.title.2005')
result_file1 = os.path.join(work_dir,'res.bm25')
result_file2 = os.path.join(work_dir,'res.tfidf')
result_file3 = os.path.join(work_dir,'res.pl2')

#engine = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir)
#run_queries(engine, query_file, result_file1)

engine2 = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir, model=0, implicit_or=False)
run_queries(engine2, query_file, result_file2)

#engine3 = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir, model=2)
#run_queries(engine3, query_file, result_file3)