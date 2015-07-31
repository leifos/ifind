__author__ = 'leif'
from threading import Thread

from django.core.cache import cache


class Worker(Thread):
    def __init__(self, query, search_engine):
        Thread.__init__(self)
        self.query = query
        self.search_engine = search_engine

    def run(self):
        key = make_key(self.query, self.search_engine)
        print "Starting " + key
        (in_cache, response) = get_response(self.query, self.search_engine)
        print "Exiting " + key


def do_cache_pages(query, search_engine, num_pages):
    for i in range(1, num_pages):
        query.skip += 1
        w = Worker(query, search_engine)
        w.setDaemon(True)
        w.start()
        print w


def get_response(query, search_engine):
    key = make_key(query, search_engine)
    response = cache.get(key)
    in_cache = True
    if not response:
        in_cache = False
        response = search_engine.search(query)
        put_results_in_cache(key, response)
    else:
        print "response fetched from cache"
    return in_cache, response


# takes a query and makes a key
def make_key(query, search_engine):
    key = ''
    top = query.top
    skip = query.skip
    terms = query.terms.strip()
    term_list = terms.split(' ')
    term_list.sort()
    terms = '-'.join(term_list)
    terms = terms.lower()
    key = search_engine.key_name + '-' + str(skip) + '-' + str(top) + '-' + terms
    print key
    return key


def get_results_from_cache(key):
    """
    returns the ifind response object, else returns None if results are not in cache
    :param key:
    :return: ifind response object
    """
    response = cache.get(key)
    return response


def put_results_in_cache(key, response):
    cache.set(key, response, None)



