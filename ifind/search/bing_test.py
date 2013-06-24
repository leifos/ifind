from ifind.search.engine.bing_web_searchv2 import BingWebSearch
from ifind.search.query import Query
import requests

query = Query('Hello World', source_type="Web", format='JSON')
query2 = Query('Hello World', source_type="Web", format='ATOM')
query3 = Query('Hello World', source_type="Web", format='JSON', top=10, skip=2)

search_engine = BingWebSearch(api_key="5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ")

result = search_engine.search(query)
result2 = search_engine.search(query2)
result3 = search_engine.search(query3)

#for r in result.result_list:
#    print r

#print

#for r in result2.result_list:
#    print r

print

for r in result3.result_list:
    print r