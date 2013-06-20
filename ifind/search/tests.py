__author__ = 'leif'


from ifind.search.tempengine import BingWebSearch
from ifind.search.query import Query
from ifind.search.response import Response

q = Query('Hello World', source='image')

se = BingWebSearch(api_key='')

r = se.search(q)

print r

print r.print_results()
print r.results_per_page