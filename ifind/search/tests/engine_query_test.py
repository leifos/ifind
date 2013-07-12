#
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
import ifind.search.engines as engines

#
engine = EngineFactory('twitter', cache_type='engine')
engine2 = EngineFactory('twitter', cache_type='engine')
#
#
query3 = Query("court", top=5, result_type='recent')
#
#
#

print engines.__path__[0]