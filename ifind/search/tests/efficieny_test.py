from ifind.search import EngineFactory
from ifind.search import Query
from ifind.search import Response

query = Query("top", top=1, result_type="")

engine = EngineFactory('wikipedia', cache='engine')
response = engine.search(query)
response = engine.search(query)


# # iterate through supported engines
# for engine in EngineFactory():
#     print engine
#
# # list of supported engines
# print EngineFactory().engines()
#
# # supported engine containment
# print 'twitter' in EngineFactory()
# print 'yahoo' in EngineFactory()