# TODO Clean up, rename and convert into BingSearch CLI module

from ifind.search.engine import EngineFactory
from ifind.search.query import Query


query = Query('one', source_type="WEB", format='atom')
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('Hello World', source_type="Web", format='JSON', top=60, skip=1)


#result = search_engine.search(query)

#for r in result.results:

engine = EngineFactory("bing", api_key='5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ')

result = engine.search(query)

for r in result.results:
    print r['title']

