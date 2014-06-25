from ifind.search import Query, EngineFactory
from keys import bing_api_key

def run_query(query):
    q = Query(query,top=6)
    e = EngineFactory("Bing", api_key=bing_api_key)

    response = e.search(q)

    return response


res = run_query(u"test")
for r in res:
    #print r.url
    #print r.rank
    #print r.title
    #print r.summary
    print r
