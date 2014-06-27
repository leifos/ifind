from ifind.search import Query, EngineFactory
from keys import bing_api_key
from models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "badsearch_project.settings")
from django.core.cache import cache, get_cache
import time, datetime

bing_engine = EngineFactory("Bing", api_key=bing_api_key)
response_cache = get_cache('default')

def mod_normal(response):
    return response

def mod_interleave(response):
    #interleaves top 20 results, returns in sequence 11, 1, 12, 3, 13, 4 etc.
    #results 21-50 are returned in original order
    results = response.results
    r = list(results)
    slice_a = slice(0,10)
    list_a = r[slice_a]
    slice_b = slice(10,20)
    list_b = r[slice_b]
    slice_c = slice(20,50)
    list_c = r[slice_c]
    list_d = []
    it=iter(list_a)

    for result in list_b:
        list_d.append(result)
        try:
            a = it.next()
            print a
            list_d.append(a)
        except StopIteration:
            break
        except Exception as e:
            raise e

    response.results = list_d + list_c
    return response

def mod_reverse(response):
    #returns results with top 20 results reversed
    results = response.results
    r = list(results)
    slice_a = slice(0,20)
    list_a = r[slice_a]
    mod_list_a = list_a[::-1]
    slice_b = slice(20,50)
    list_b = r[slice_b]
    response.results = mod_list_a + list_b

    return response

conditions = {
    1: mod_normal,
    2: mod_reverse,
    3: mod_interleave
}

def get_user_condition(request):
    user_id = request.user.id
    if user_id % 2 is 0:
        condition=1
    elif user_id % 2 is not 0:
        condition=2
    return condition

def run_query(query, condition):
    q = Query(query, top=50)

    # check cache, if query is there, return results
    # else send query to bing, and store the results in the cache
    response = bing_engine.search(q)
    mod = conditions[condition]
    mod_response = mod(response)

    return mod_response

def paginated_search(request, query):
    condition = get_user_condition(request)

    if query:

            if not response_cache.get(query):
                response = run_query(query, condition=3)
                response_cache.set(query, response)

            else:
                response = response_cache.get(query)
                print "cached query present"

            paginator = Paginator(response.results, 10)
            page = request.REQUEST.get('page')

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # if page not an integer, deliver first page
                results = paginator.page(1)
            except EmptyPage:
                # if page out of range, deliver last page of results
                results = paginator.page(paginator.num_pages)

            return results

