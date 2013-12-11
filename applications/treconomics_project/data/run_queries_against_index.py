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
        print "BM25"
    else:
        if (s == 2):
            w = scoring.PL2(c=10.0)
            print "PL2"
        else:
           w = scoring.BM25F(B=0.75, K1=1.5) 
           print "BM25"
    return w


work_dir = os.getcwd()
my_whoosh_doc_index_dir = os.path.join(work_dir, 'fullindex')

query_file = "queries.trec.title.2005"
result_file = "res.aq_title_bm25_or"
max_results = 1000

print "Opening Index: " +  my_whoosh_doc_index_dir
ix = open_dir( my_whoosh_doc_index_dir )
ixr = ix.reader()
#qp = MultifieldParser(["title", "content"], schema=ix.schema)
qp = qparser.QueryParser("content", schema=ix.schema, group=qparser.OrGroup)
#qp.add_plugin(qparser.MultifieldPlugin(["title", "content"] ) )

sf = createScoreFunction( 1 )

infile = open(query_file,"r")
outfile = open(result_file,"w")
while infile:
    line = infile.readline()
    parts = line.partition(' ')
            
    query_num = parts[0]
    query_str = unicode( parts[2] )
    max_limit = 1000
    whoosh_query =  qp.parse(query_str)
    with ix.searcher( weighting=sf ) as searcher:
        
        docscore = {}
        for q in whoosh_query:
            print q.fieldname
            print q.text
            
            p = searcher.postings(q.fieldname,q.text)
         
            for i in p.all_ids():
                #print i, p.score()
                if i in docscore:
                    docscore[i] =+ p.score()
                else:
                    docscore[i] = p.score()
                    
        results = []
        n = len(docscore)
        if n > max_results:
            n = max_results
        if n > max_limit:
            n = max_limit
            
        sorted_ds = sorted(docscore.iteritems(), key=operator.itemgetter(1))    

        print query_num + " " + str(len(results)) + " " + str(n)
        #if n > 0:
        #    for rank in range(n):
        #        print sorted_ds[0], sorted_ds[1]
                #trec_line = query_num + " Q0 " + [rank]["docid"] + " " + str( rank + 1 ) + " " + str(results[rank].score) + " Exp\n"
                #outfile.write(trec_line)
        
        if not line:
            break
                

