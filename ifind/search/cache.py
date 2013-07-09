### TEST CODE ###

import os
import redis
import pickle
import base64
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
        self.cache_type = cache_type or 'engine'

        self.connection = RedisConn(host=self.host, port=self.port, db=self.db).connect()

    def make_key(self, query):

        if self.cache_type.lower() == 'engine':
            return "QueryCache::{0}::{1}".format(self.engine_name, hash(query))
        if self.cache_type.lower() == 'instance':
            return "QueryCache::{0}::{1}".format(id(self), hash(query))

    def get_set_name(self):

        if self.cache_type.lower() == 'engine':
            return "QueryCache::{0}-keys".format(self.engine_name)
        if self.cache_type.lower() == 'instance':
            return "QueryCache::{0}-keys".format(id(self))

    def store(self, query, response, expires=None):

        key = self.make_key(query)
        value = base64.b64encode(pickle.dumps(response))
        set_name = self.get_set_name()

        while self.connection.scard(set_name) >= self.limit:
            self.connection.spop(set_name) # random deletion atm, not great

        if expires is None:
            expires = self.expires

        pipe = self.connection.pipeline()
        pipe.setex(key, expires, value)  # rework expiry to use scoring, maybe, find out requirements
        pipe.sadd(set_name, key)
        pipe.execute()

    def get(self, query):

        key = self.make_key(query)
        set_name = self.get_set_name()

        if key in self:
            value = self.connection.get(key)
            if value is None:  # expired
                self.connection.srem(set_name, key)
                raise SearchException(MODULE, "cache: {0} key: {1} has expired".format(set_name, key))
            return pickle.loads(base64.b64decode(value))

        raise SearchException(MODULE, "cache: {0) key: {1}".format(set_name, key))

    def __contains__(self, key):
        return self.connection.sismember(self.get_set_name(), key)


#   1. Engine is instantiated and an optional cache parameter can be supplied
#
#           If cache='instance' then only cached responses keyed to that instance will be returned
#           If cache='engine' then only cached responses keyed to that engine will be returned
#           If cache=None then nothing happens with regards to caching
#
#   2. Engine's constructor creates a QueryCache object and self.cache references that.
#
#           Inside QueryCache you'd have the following attributes/methods:
#
# l             imit: no of encoded strings (responses) to cache
#               expire: key expiry time in seconds
#               host: redis host
#               port: redis port
#               db: redis db number
#               connection: uses simple connection object to establish redis connection
#
#               make_key(self,key): returns key
#                                   if 'engine' then something like:    "QueryCache::<Engine>::<query_key>"
#                                   if 'instance' then something like:  "QueryCache::<Engine><ID>::<query_key>"
#
#               get_set_key(self): generates the key set for engine/instance
#                                   if 'engine' then something like:     "QueryCache::<Engine>::keys"
#                                   if 'instance' then something like:   "QueryCache::<Engine><ID>::keys"
#
#               store(self, key, value, expire=None): stores a key/value after space manipulations
#                                   get key, value, name of set
#                                   check space, make space?
#                                   create redis pipeline
#                                   set expiry, add key/value and execute pipeline
#
#               store_pickle(self, key, value): pickles, encodes and stores in cache











# Due to nature of QueryCache being an attachable object, I'm assuming non-persistence.
# i.e. When Engine instance deleted/dereferenced the cache is cleared too (regardless of engine/instance specific)
# If persistence is wanted (which you'd likely want with cached='engine' you can do it with a QueryCache object but is
# redundant.

# ALL QUERYCACHE OBJECTS ARE GOING TO BE MAKING THE SAME CALLS TO REDIS REGARDLESS (unless QueryCache has a fallback
# local dict cache.

# What you'd probably want ultimately is singleton QueryCaches for every engine.
#
#
# Twitter Engine -------> TwitterQueryCache
# Twitter Engine -------> TwitterQueryCache
#
# but instead have..
#
# Twitter Engine ------>
# Twitter Engine -------> TwitterQueryCache
# Twitter Engine ------>