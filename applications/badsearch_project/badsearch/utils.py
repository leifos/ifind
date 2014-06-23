from ifind.search import Query, EngineFactory
from keys import bing_api_key

bing_engine = EngineFactory("Bing", api_key=bing_api_key)

def mod_normal(results):
    return results

def mod_slow(results):
    return results

def mod_bad(results):
    #returns results in reverse order
    r = list(results)
    mod_r = r[::-1]
    return mod_r

conditions = {
    1: mod_normal,
    2: mod_slow,
    3: mod_bad
}

def run_query(query, condition=3):
    q = Query(query, top=50)
    response = bing_engine.search(q)
    mod = conditions[condition]
    mod_results = mod(response)

    return mod_results

