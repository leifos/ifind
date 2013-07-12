from ifind.search import EngineFactory
from ifind.search import Query
from ifind.search import Response


engine = EngineFactory('twitter')
query = Query("test harness", top=3)


# iterate through supported engines
for engine in EngineFactory():
    print engine

# list of supported engines
print EngineFactory().engines()

# supported engine containment
print 'twitter' in EngineFactory()
print 'yahoo' in EngineFactory()