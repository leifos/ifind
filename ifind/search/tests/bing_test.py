# TODO Clean up, rename and convert into BingSearch CLI module

from ifind.search.engine import EngineFactory
from ifind.search.query import Query
import redis


#query = Query('test', source_type="WEB", format='ATOM')
#query = Query('Hello World', source_type="Web", format='ATOM')
query = Query('chicken', source_type="Web", format='JSON', top=30, skip=0)
query2 = Query('chicken', source_type="Web", format='JSON', top=10, skip=400)

engine = EngineFactory("bing", api_key='5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ')

result = engine.search(query)
result2 = engine.search(query2)

#r_server = redis.Redis("localhost")

for i, r in enumerate(result.results):
    print i, r['title']
    #r_server.sadd('result25', r['url'])

print

for i, r in enumerate(result2.results):
    print i, r['title']
    #r_server.sadd('result26', r['url'])

#print r_server.scard('result25')
#print r_server.scard('result26')

#r_server.sinter('dog', 'dogg')