### TEST CODE ###

import os
import redis
import pickle
import base64
from time import strftime, gmtime
from ifind.search.engines.exceptions import SearchException, EngineException

MODULE = os.path.basename(__file__).split('.')[0].title()
CACHE_TYPES = ('engine', 'instance')

#   SearchEngine can be created with or without a QueryCache
#
#   QueryCache stores query response (
#   (stores the number of times the query has been retrieved, and last retrieved)
#
# - with a QueryCache, the search method of SearchEngine should:
#     - check if their is a QueryCache,
#         if query is in cache,
#           return response
#         else:
#           perform search request
#           store response in cache
#


class RedisConn(object):

    def __init__(self, host="localhost", port=6379, db=0):

        self.host = host
        self.port = port
        self.db = db

    def connect(self):

        try:
            redis.StrictRedis(host=self.host, port=self.port).ping()
        except redis.ConnectionError:
            raise SearchException(MODULE, "Failed to establish connection to "
                                          "redis server @ {0}:{1}".format(self.host, self.port))

        return redis.StrictRedis(host=self.host, port=self.port, db=self.db)


class QueryCache(object):

    def __init__(self, engine, host='localhost', port=6379, db=0,
                 limit=1000, expires=60 * 60 * 24, cache_type=None):

        self.engine_name = engine.name.lower()

        self.host = host
        self.port = port
        self.db = db

        self.limit = limit
        self.expires = expires
        self.cache_type = cache_type

        self.connection = RedisConn(host=self.host, port=self.port, db=self.db).connect()

    def store(self, query, response, expires=None):

        # check limits

        if expires is None:
            expires = self.expires

        key = self._make_key(query)
        value = base64.b64encode(pickle.dumps(response))

        pipe = self.connection.pipeline()
        pipe.hmset(key, {'response': value, 'count': 0, 'last': ''})
        pipe.expire(key, expires)
        pipe.execute()

    def get(self, query):

        key = self._make_key(query)
        value = self.connection.hget(key, 'response')

        if value:

            pipe = self.connection.pipeline()
            pipe.hincrby(key, 'count', 1)
            pipe.hset(key, 'last', strftime("%Y/%m/%d %H:%M:%S", gmtime()))
            pipe.execute()

            return pickle.loads(base64.b64decode(value))

        else:

            return None

    def _make_key(self, query):

        if self.cache_type.lower() == 'engine':
            return "QueryCache::{0}::{1}".format(self.engine_name, hash(query))
        if self.cache_type.lower() == 'instance':
            return "QueryCache::{0}::{1}".format(id(self), hash(query))

    def __contains__(self, query):
        return self.connection.exists(self._make_key(query))