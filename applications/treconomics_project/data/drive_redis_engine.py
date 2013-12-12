import os
from ifind.search.query import Query
from ifind.search.engines.whooshtrecnewsupdated import WhooshTrecNews


work_dir = os.getcwd()
whoosh_index_dir = os.path.join(work_dir, 'fullindex')

query = Query(terms='banana monkey', top=10)
query.skip=1
query.top = 10
engine = WhooshTrecNews(whoosh_index_dir=whoosh_index_dir)

response = engine.search(query)

for res in response:
	print res.docid



"""
# Add the total number of pages from the results object as an attribute of our response object.
# We also add the total number of results shown on the page.
setattr(response, 'total_pages', results.pagecount)
setattr(response, 'results_on_page', results.pagelen)
setattr(response, 'actual_page', results.actual_page)
return response
"""