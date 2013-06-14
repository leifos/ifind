__author__ = 'jpurvis'
from pagefetch.service import service

from puppy.model import Query, Response


def test():
    user_query = "bing test"
    results = service.search_services['bing_web'].search( Query(user_query) )
    print results

test()
