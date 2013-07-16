from __future__ import with_statement
from ifind.search.tests import gen_query
from ifind.search import *
import time


class Timer(object):

    def __enter__(self):
        self.__start = time.time()

    def __exit__(self, type, value, traceback):
        self.__finish = time.time()

    def duration_in_seconds(self):
        return self.__finish - self.__start


def time_requests(query_amount):

    query_list = [query for query in gen_query(count=query_amount)]

    engine = EngineFactory('bing', api_key="5VP0SQJkCyzkT1GfsWT//q4pt1zxvyaVVhltoDhfTDQ", cache='instance')

    def time():
        timer = Timer()
        with timer:
            for query in query_list:
                engine.search(query)
        return timer.duration_in_seconds()

    non_cache_time = time()
    cached_time = time()

    return {'cached': cached_time, 'non_cached': non_cache_time }

query_amount = 10

non_cache_times = []
cached_times = []

for i in xrange(3):

    results = time_requests(query_amount)
    non_cache_times.append(results['non_cached'])
    cached_times.append(results['cached'])

print 'Bing -- {0} queries -- non-cached -- {1}s'.format(query_amount, sum(non_cache_times) / len(non_cache_times))
print 'Bing -- {0} queries -- cached     -- {1}s'.format(query_amount, sum(cached_times) / len(cached_times))