import mock
import random
from ifind.search import *

MODULE_PATH = "/".join(__file__.split('/')[:-1])


def gen_query(count=1, response=False):
    """
    Utility generator that yields 'count' query/response pairs, randomly generated.

    """
    with open('{}/word_list.txt'.format(MODULE_PATH), 'r') as word_list_file:
        word_list = word_list_file.readlines()

        for i in xrange(count):
            query = Query(random.choice(word_list).strip())
            resp = Response(query.terms)

            if response:
                yield query, resp
            else:
                yield query


def create_engine(name, cache_type):
    """
    Utility function to return mocked engine instance object.

    """
    engine = mock.Mock()
    engine.name = name
    engine.cache_type = cache_type
    return engine