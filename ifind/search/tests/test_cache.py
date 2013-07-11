from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises

import ifind.search.cache as cache
from ifind.search.engine import EngineFactory
from exceptions import DynamicException

class TestCache(object):

    def setup(self):
        engine = EngineFactory("twitter")
        #self.c = cache.QueryCache(engine)
        assert_raises(DynamicException, cache.QueryCache, engine)


    def test_cache(self):
        assert_raises(DynamicException, EngineFactory, "bing")
        pass