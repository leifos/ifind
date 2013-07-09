
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
#from ifind.search.cache import *

#query = Query('dog', top=10)
query = Query('glasgow', top=5)
#query2 = Query('glasgow', top=10)
#query = Query('awful bus glasgow', source_type="Web", format='JSON', top=10, skip=0)
#query2 = Query('milk death', result_type="web", format='JSON', top=70, skip=0)
#query2 = Query("furnace", result_type='recent', top=5)

#raise SearchException(__file__.split('/')[-1].split('.')[0], "PROBLEM")

#engine = EngineFactory('wikipedia', cache_type='engine')

#print engine._cache.cache_type

#response = engine.search(query)

#engine._cache.store(query, response)

#response = engine._cache.get(query)

engine2 = EngineFactory('wikipedia')

query20 = Query('martin', top=10)
query20.terms = 'glasgow'
query20.top = 5

#response = engine2.search(query20)

response = engine2._cache.get(query20)

print response

