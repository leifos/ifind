import mock
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises

import ifind.search.cache as cache
from ifind.search.query import Query
from ifind.search.response import Response
from ifind.search.exceptions import CacheConnectionException


class TestEngineCache(object):

    def setup(self):

        self.engine = mock.Mock()
        self.engine.name = "TestEngine"
        self.engine.cache_type = "Engine"

        self.c = cache.QueryCache(self.engine)
        self.c.connection.flushdb()

        self.query = Query('hello world')
        self.response = Response('hello world')

    def test_bad_connection(self):
        assert_raises(CacheConnectionException, cache.QueryCache, self.engine, host='badness')

    def test_expires(self):
        import time

        self.c.connection.flushdb()

        self.c.store(self.query, self.response, expires=1)
        time.sleep(1.1)

        assert_equal(self.c.get(self.query), None)

    def test_limit(self):
        self.c.limit = 1
        query2 = Query('hello david')
        response2 = Response("hello david")
        self.c.store(self.query, self.response)
        self.c.store(query2, response2)
        assert_equal(self.c.connection.zcard(self.c.set_name), self.c.limit)

    def test_store_retrieve(self):
        self.c.store(self.query, self.response)
        assert_equal(self.response, self.c.get(self.query))


class TestInstanceCache(TestEngineCache):

    def setup(self):

        self.engine = mock.Mock()
        self.engine.name = "TestEngine"
        self.engine.cache_type = "Instance"

        self.c = cache.QueryCache(self.engine)
        self.c.connection.flushdb()
        
        self.query = Query('hello world')
        self.response = Response('hello world')