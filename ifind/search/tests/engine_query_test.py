#
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
# from ifind.search.cache import *
#
#
engine = EngineFactory('govuk')
#
#
query3 = Query("court", top=3)
#
#
#
response = engine.search(query3)
#
# print response