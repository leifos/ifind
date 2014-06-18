__author__ = 'Craig'

import time
from ifind.search import Query, EngineFactory
from keys import BING_API_KEY

e = EngineFactory("Bing", api_key=BING_API_KEY)


def mod_normal(results):
    return results


def mod_slow(results):
    time.sleep(5)
    return results


def mod_bad(results):
    return results

conditions = {
    1: mod_normal,
    2: mod_slow,
    3: mod_bad
}


# run a search query on Bing using the query string passed
def run_query(query, condition=2):
    q = Query(query, top=10)

    response = e.search(q)

    print 'modding results'
    mod = conditions[condition]
    mod_results = mod(response)

    return mod_results


