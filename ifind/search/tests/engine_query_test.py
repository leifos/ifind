import requests
import xml.dom.minidom
from ifind.search.engine import EngineFactory
from ifind.search.query import Query

query = Query('test', result_type="WEB", format='JSON')
#query = Query('Hello World', source_type="Web", format='ATOM')
#query = Query('awful bus glasgow', source_type="Web", format='JSON', top=10, skip=0)
#query2 = Query('milk death', result_type="web", format='JSON', top=70, skip=0)
#query2 = Query("furnace", result_type='recent', top=5)

engine = EngineFactory("bing", api_key='')


#response = engine.search(query)

#for index, result in enumerate(response):
    #print index
    #print result


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

terms = "dog"

search_params = {'format': 'xml',
                 'search': terms,
                 'action': 'opensearch'}

response = requests.get('http://www.wikipedia.org/w/api.php', params=search_params)


xmldoc = xml.dom.minidom.parseString(response.content)

print xmldoc.toprettyxml()

items = xmldoc.getElementsByTagName('Item')

for item in items:

    title = item.getElementsByTagName('Text')[0].firstChild.data
    url = item.getElementsByTagName('Url')[0].firstChild.data
    summary = item.getElementsByTagName('Description')[0].firstChild.data

    print title
    print summary
    print url