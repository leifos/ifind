# TODO Clean up, rename and convert into BingSearch CLI module

from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query

query = Query('Hello Worldlings of doom', source_type="Web", format='JSON')
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('Hello World', source_type="Web", format='JSON', top=60, skip=1)

search_engine = BingWebSearch(api_key='')

result = search_engine.search(query)

for r in result.results:
    print r['url']

