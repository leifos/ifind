# TODO Clean up, rename and convert into BingSearch CLI module

import ifind.search.search as search

from ifind.search.search import Engine

from ifind.search.query import Query

query = Query('Hello Worldlings of doom', source_type="Web", format='JSON')
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('Hello World', source_type="Web", format='JSON', top=60, skip=1)


#result = search_engine.search(query)

#for r in result.results:

engine = Engine("DUMMY", api_key='')

result = engine.search(query)

for r in result.results:
    print r['title']