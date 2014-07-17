import os
import timeit
from ifind.search.query import Query
from ifind.search.engines.whooshtrecnewsredis import WhooshTrecNewsRedis

# Paths
work_dir = os.getcwd()
whoosh_index_dir = os.path.join(work_dir, 'fullindex')
query_file = os.path.join(work_dir, '347.iiix2014.queries')

# Settings
skip = 1
top = 10
ignore_terms = ['and', 'or', 'not']

# Engine
engine = WhooshTrecNewsRedis(whoosh_index_dir=whoosh_index_dir, use_cache=False)

def get_query_list():
	input_file = open(query_file, 'r')
	query_list = []
	
	for line in input_file:
		line = line.strip()
		line = line.partition(' ')
		
		query = line[2]
		query = query.strip()
		query = query.lower()
		query = query.replace('"', '')
		
		query = query.split()
		new_query = ""
		
		for term in query:
			if term not in ignore_terms:
				new_query = new_query + term + ' '
		
		new_query = new_query.strip()
		query_list.append(new_query)
	
	input_file.close()
	return query_list

query_list = get_query_list()

for query in query_list:
	query_obj = Query(terms=query, top=top)
	query_obj.skip = skip
	
	start_time = timeit.default_timer()
	
	results = engine.search(query_obj)
	
	print
	print "Query '{0}' executed in {1:.2f} seconds".format(query, (timeit.default_timer() - start_time))
	print "Got {0} result(s)".format(len(results))
	print