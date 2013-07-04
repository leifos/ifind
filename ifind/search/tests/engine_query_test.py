import requests
import xml.dom.minidom
from ifind.search.engine import EngineFactory
from ifind.search.query import Query

query = Query('test', result_type="Web", format='JSON', top=70)
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('awful bus glasgow', source_type="Web", format='JSON', top=10, skip=0)
#query2 = Query('milk death', result_type="web", format='JSON', top=70, skip=0)
#query2 = Query("furnace", result_type='recent', top=5)

engine = EngineFactory("bing", api_key='5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ')


response = engine.search(query)


for index, result in enumerate(response):
    print index
    print result


# result2 = engine.search(query2)
# #result += result2
#
# #r_server = redis.Redis("localhost")
#
# for i, r in enumerate(result.results):
#     print i+1, r['title']
#     #r_server.sadd('result25', r['url'])
#
# print
#
# for i, r in enumerate(result2.results):
#     print i+1, r['title']
#     #r_server.sadd('result26', r['url'])
#
# #print r_server.scard('result25')
# #print r_server.scard('result26')
#
# #r_server.sinter('dog', 'dogg')

#/
    #slug = re.findall(r'')

#items = xml.getElementByTagName('Item')