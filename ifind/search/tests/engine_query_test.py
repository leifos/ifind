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
query3 = Query("court", top=3)
#
#
#
response = engine.search(query3)
#

pprint.pprint(json.loads(response.to_json()))