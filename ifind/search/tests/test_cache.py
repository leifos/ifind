import mock
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises

import ifind.search.cache as cache
from ifind.search.query import Query
from ifind.search.response import Response


class TestCache(object):

    def setup(self):

        engine = mock.Mock()
        engine.name = "TestEngine"
        engine.cache_type = 'engine'

        self.c = cache.QueryCache(engine)
        self.query = Query('hello world')
        self.response = Response('hello world')

    def test_expires(self):
        import time
        self.c.store(self.query, self.response, expires=1)
        time.sleep(1.1)
        assert_equal(self.c.get(self.query), None)

    def test_store_retrive(self):
        self.c.store(self.query, self.response)
        assert_equal(self.response, self.c.get(self.query) )