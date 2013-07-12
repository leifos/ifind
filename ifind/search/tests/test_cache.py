import mock
import string
import random

from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises

import ifind.search.cache as cache
from ifind.search.query import Query
from ifind.search.response import Response
from ifind.search.exceptions import CacheConnectionException


class TestEngineCache(object):
    """
    Test suite for QueryCache using an 'engine' cache type.

    """
    def setup(self):
        """
        Creates engine, cache and a query/response pair as instance attributes.

        """
        # mock engine
        self.engine = create_engine("TestEngine", "engine")

        # create cache and flush db
        self.c = cache.QueryCache(self.engine)
        self.c.connection.flushdb()

        # create default query/response test pair
        for pair in gen_query_response():
            self.query, self.response = pair

    def test_bad_connection(self):
        """
        Checks exception thrown when unable to connect to redis backend.

        """
        # connect to bad hostname, check exception
        assert_raises(CacheConnectionException, cache.QueryCache, self.engine, host='badness')

    def test_expires(self):
        """
        Checks that a cache key expires within the given time.

        """
        import time

        # store query/response with a 1 second expiry
        self.c.store(self.query, self.response, expires=1)

        # wait just over a second
        time.sleep(1.1)

        # check to see that key has expired
        assert_equal(self.c.get(self.query), None)

    def test_limit(self):
        """
        Checks that cache size (limit) integrity is maintained.

        """
        import random

        # set random limit
        self.c.limit = random.randint(0, 100)
        variance = random.randint(1, 6)

        # generate too many response/query pairs and store in cache
        for pair in gen_query_response(self.c.limit + variance):
            self.c.store(pair, None)

        # check to see that limit matches key set cardinality
        assert_equal(self.c.connection.zcard(self.c.set_name), self.c.limit)

    def test_store_retrieve(self):
        """
        Checks that a query can be restored and retrieved from cache.

        """
        # store query/response
        self.c.store(self.query, self.response)
        # check that cached response matches original
        assert_equal(self.c.get(self.query), self.response)

    def test_already_stored(self):
        """
        Checks that adding an already cached query/response doesn't break anything.

        """
        # store query/response
        self.c.store(self.query, self.response)
        # check that nothing has returned
        assert_equal(self.c.store(self.query, self.response), None)

    def test_cache_persistence(self):
        """
        Checks that cache persistence behaviour is maintained.

        i.e. New engines use same cache as type is 'engine'.

        """
        # create engine with identical attributes to default engine
        engine = create_engine(self.engine.name, self.engine.cache_type)
        # create new cache for engine
        c = cache.QueryCache(engine)
        # store instance query/response
        c.store(self.query, self.response)

         # create 2nd engine with identical attributes to default engine
        engine2 = create_engine(self.engine.name, self.engine.cache_type)
        # create new cache for engine
        c2 = cache.QueryCache(engine2)
        # check that new cache has query/response available
        assert_equal(c2.get(self.query), self.response)

    def teardown(self):
        self.c.connection.flushdb()


class TestInstanceCache(TestEngineCache):
    """
    Identical test suite for QueryCache except using an 'instance' cache type.

    """
    def setup(self):
        """
        Creates engine, cache and a query/response pair as instance attributes.

        Notes:
            Overridden method.

        """
        self.engine = create_engine("TestEngine", "instance")

        self.c = cache.QueryCache(self.engine)
        self.c.connection.flushdb()

        for pair in gen_query_response():
            self.query, self.response = pair

    def test_cache_persistence(self):
        """
        Checks that cache persistence behaviour is maintained.

        i.e. New engines use new/volatile cache as type is 'instance'.

        Notes:
            Overridden method.

        """
        # create engine with identical attributes to default engine
        engine = create_engine(self.engine.name, self.engine.cache_type)
        # create new cache for engine
        c = cache.QueryCache(engine)
        # store instance query/response
        c.store(self.query, self.response)

         # create 2nd engine with identical attributes to default engine
        engine2 = create_engine(self.engine.name, self.engine.cache_type)
        # create new cache for engine
        c2 = cache.QueryCache(engine2)
        # check that new cache does not have query/response available
        assert_equal(c2.get(self.query), None)


def gen_query_response(count=1):
    """
    Utility generator that yields 'count' query/response pairs, randomly generated.

    """
    for x in xrange(count):
        length = random.randint(1, 10)
        query = Query(''.join(random.choice(string.lowercase) for x in xrange(length)))
        response = Response(query.terms)
        yield query, response


def create_engine(name, cache_type):
    """
    Utility function to return mocked engine instance object.

    """
    engine = mock.Mock()
    engine.name = name
    engine.cache_type = cache_type
    return engine