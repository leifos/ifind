from ifind.search.engine.bing_web_search import BingWebSearch
from ifind.search.query import Query

q = Query('Hello World', source='image')

se = BingWebSearch(api_key='5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ')

r = se.search(q)

print r

print r.print_results()
