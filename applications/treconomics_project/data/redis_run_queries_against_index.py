from whoosh import scoring
from whoosh.index import open_dir
from whoosh.qparser import QueryParser, OrGroup, AndGroup
import operator
import os
from ifind.search.cache import RedisConn


def create_scoring_function(s):
	"""
	Returns a scoring function object, depending of the value of s.
	"""
	if s == 2:
		w = scoring.PL2(c=10.0)
	else:
		w = scoring.BM25F(B=0.75, K1=1.5)
	
	return w

def get_query(query_parser, query_string):
	"""
	To get around a NotImplementedError in the Whoosh library (sigh), checks the query string provided.
	Returns the string if only one term is contained. Otherwise, returns a Whoosh compound query.
	"""
	if len(query_string.split()) == 1:
		return unicode(query_string)
	
	return query_parser.parse(query_string)

def update_scores(doc_scores, doc_term_scores):
	"""
	Given a document scores hashmap and set of postings, updates the document scores hashmap.
	The updated hashmap contains cumulative scores.
	"""
	for i in doc_term_scores:
		if i in doc_scores:
			doc_scores[i] = doc_scores[i] + doc_term_scores[i]
		else:
			doc_scores[i] = doc_term_scores[i]


def make_key(field_name,term):
    key = '%s:%s' % ( field_name, term)
    return key


def get_postings_from_redis(rc, field_name, term):
    values = rc.get(make_key(field_name,term))
    return values
    
def set_postings_to_redis(rc, field_name, term, values):
    key = make_key( field_name, term)
    rc.store(key,values)

#  Settings
max_limit = 1000  # The maximum number of documents to return
grouping = OrGroup  # How do we group terms in our query?
field_name = 'content'  # Which field are we using?
scoring_function = create_scoring_function(2)  # Which function should we use to score docs?

#  Get paths to the necessary files/directories
work_dir = os.getcwd()
whoosh_index_dir = os.path.join(work_dir, 'fullindex')
query_file = os.path.join(work_dir, '435.sigir2013.queries')
result_file = os.path.join(work_dir, 'res.redis_pl2_or.435')

#  Open the index and necessary Whoosh ancillaries
ix = open_dir(whoosh_index_dir)
reader = ix.reader()
query_parser = QueryParser(field_name, schema=ix.schema, group=grouping)
print ix.schema

#  Open the input and output files for reading and writing
input_file = open(query_file, 'r')
output_file = open(result_file, 'w')


#Create a Redis Connection

rc = RedisConn()
rc.connect()


for line in input_file:
	line = line.strip()  # Remove the endline character
	line = line.partition(' ')
	
	query_num = line[0]
	query_string = line[2].strip()
	
	whoosh_query = get_query(query_parser, query_string)
	
	with ix.searcher(weighting=scoring_function) as searcher:
		doc_scores = {}
		
		print whoosh_query
		
		#  If a single term is provided as the query, we get NotImplementedError exceptions in the Whoosh library!
		#  To avoid this, check if the query returned is unicode - if it is, there's one term only - if not, there's >1 term.
		if isinstance(whoosh_query, unicode):
			doc_term_scores = {}
			try:
				postings = searcher.postings(field_name, whoosh_query)
				for i in postings.all_ids():
					doc_term_scores[i] = postings.score()
			except:
				pass
			update_scores(doc_scores, doc_term_scores)
		else:
			for term in whoosh_query:
				doc_term_scores = {}
				key =  make_key(term.fieldname,term.text) 
				print rc
				if rc.exists(key):
					doc_term_scores = get_postings_from_redis(rc, term.fieldname, term.text)
				else:
					try:
						postings = searcher.postings(term.fieldname, term.text)
						for i in postings.all_ids():
							doc_term_scores[i] = postings.score()
					except:
						pass
						
					set_postings_to_redis(rc, term.fieldname,term.text, doc_term_scores)
					
				update_scores(doc_scores, doc_term_scores)				   
		
		results = []
		n = len(doc_scores)
		
		if n > max_limit:
			n = max_limit
		
		ranked_results = sorted(doc_scores.iteritems(), key=operator.itemgetter(1), reverse=True)
		
		print "{0}  {1}  {2}".format(query_num, len(ranked_results), n)
		
		if n > 0:
			for rank in range(n):
				trec_docid = reader.stored_fields(ranked_results[rank][0])['docid']
				score_formatted = "{0:.6f}".format(ranked_results[rank][1])
				output_file.write("{0} Q0 {1} {2} {3} Exp{4}".format(query_num, trec_docid, (rank + 1), score_formatted, os.linesep))

ix.close()
input_file.close()
output_file.close()