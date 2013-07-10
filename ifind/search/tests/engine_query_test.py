
from ifind.search.engine import EngineFactory
from ifind.search.query import Query
from ifind.search.cache import *


engine = EngineFactory('wikipedia', cache_type='engine')


query3 = Query("grantham", top=5)

engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)
engine.search(query3)