__author__ = 'Craig'
from ifind.search import Query, EngineFactory

q = Query("Google", top=5)
e = EngineFactory("Wikipedia")

print q
print e

response = e.search(q)

for r in response.results:
    print r
