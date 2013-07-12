#
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
import pprint
import json
# from ifind.search.cache import *
#
#
engine = EngineFactory('twitter')
#
#
query3 = Query("court", top=5, result_type='recent')
#
#
#
response = engine.search(query3)
response2 = engine.search(query3)

print response2 == response