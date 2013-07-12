#
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
from ifind.search.response import Response
import random, string
#
#
engine = EngineFactory('twitter', cache_type='engine')
engine2 = EngineFactory('twitter', cache_type='engine')
#
#
query3 = Query("court", top=5, result_type='recent')
#
#
#


def gen_query_response(length=8):
    query = Query(''.join(random.choice(string.lowercase) for x in xrange(length)))
    response = Response(query.terms)
    yield query, response




engine2.search(query3)