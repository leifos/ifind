from ifind.search import Query, EngineFactory

def run_query(query):
    q = Query(query)
    e = EngineFactory("Wikipedia")

    response = e.search(q)

    return response