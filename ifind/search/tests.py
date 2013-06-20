__author__ = 'leif'


from ifind.search.tempengine import BingWebSearch
from ifind.search.query import Query
from ifind.search.response import Response

q = Query('Hello World', format="ATOM")

se = BingWebSearch(api_key='/aROdM5Ck7fKHR4ge30r8W/K/D84GJkcl42lL8eNMSc=')

r = se.search(q)

print r

print r.print_results()
print r.results_per_page