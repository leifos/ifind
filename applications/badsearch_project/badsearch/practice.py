from ifind.search import Query, EngineFactory
from keys import bing_api_key

def run_query(query):
    q = Query(query)
    e = EngineFactory("Bing", api_key=bing_api_key)

    response = e.search(q)

    return response