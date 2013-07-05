from ifind.search.engines.exceptions import SearchException
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
#from ifind.search.cache import *

#query = Query('dog', top=10)
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('awful bus glasgow', source_type="Web", format='JSON', top=10, skip=0)
#query2 = Query('milk death', result_type="web", format='JSON', top=70, skip=0)
#query2 = Query("furnace", result_type='recent', top=5)

#raise SearchException(__file__.split('/')[-1].split('.')[0], "PROBLEM")

#engine = EngineFactory("twitter")

#response = engine.search(query)

query = Query('Hello World', source_type="Web", format='ATOM')
query2 = Query('awful bus glasgow', source_type="Web", format='JSON')

query2.terms = 'Hello World'
query2.format = "ATOM"


print query == query2