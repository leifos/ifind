import os
import redis
from ifind.search.engines.exceptions import SearchException, EngineException

MODULE = os.path.basename(__file__).split('.')[0].title()

HOST = 'localhost'
PORT = 6379
DB = 0

try:
    redis.StrictRedis(host=HOST, port=PORT).ping()
except redis.ConnectionError:
    raise SearchException(MODULE, "Failed to establish connection to redis server @ {0}:{1}".format(HOST, PORT))







 # QueryCache object created from Engine, imported from here
 # Eventually create connection class
 # For now have all constructed QueryCache objects steal the connection data from global scope
 # Mirror simple cache for now
 # Let's go!




     # - a SearchEngine can be created with or without a QueryCache
    #
    # - QueryCache stores the (Query, Response) pairs (and the number of times the query has been retrieved, and last retrieved)
    #
    # - with a QueryCache, the search method of SearchEngine should:
    #     - check if their is a QueryCache,
    #         if so, check if the exact query is in cache,
    #             if so, return response
    #             else,
    #                 perform search request
    #                 store results in cache
    #         else
    #             perform search request
    #             store results in cache