import os
from ifind.search.query import Query
from ifind.search.engines.whooshtrecnewsupdated import WhooshTrecNews


work_dir = os.getcwd()
whoosh_index_dir = os.path.join(work_dir, 'fullindex')

query = Query(terms='hello monkey banana', top=10)
engine = WhooshTrecNews(whoosh_index_dir=whoosh_index_dir)
engine.search(query)