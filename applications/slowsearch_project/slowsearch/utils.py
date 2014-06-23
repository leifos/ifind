__author__ = 'Craig'

import time
from ifind.search import Query, EngineFactory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from keys import BING_API_KEY

e = EngineFactory("Bing", api_key=BING_API_KEY)

delay_time = 5


def mod_normal(results):
    return results


def mod_slow(results, delay=delay_time):
    time.sleep(delay)
    return results


def mod_bad(results):
    return results

conditions = {
    1: mod_normal,
    2: mod_slow,
    3: mod_bad
}


# run a search query on Bing using the query string passed
def run_query(query, condition):
    q = Query(query, top=100)

    response = e.search(q)

    mod = conditions[condition]
    mod_results = mod(response)

    return mod_results


def paginated_search(request, query):
    cnd = get_condition(request)
    if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query, cnd)

            paginator = Paginator(result_list.results, 10)  # show 10 results per page

            #get the page number required from the request
            page = request.REQUEST.get('page')

            try:
                contacts = paginator.page(page)
            except PageNotAnInteger:
                # if page not an integer, deliver first page
                contacts = paginator.page(1)
            except EmptyPage:
                # if page out of range, deliver last page of results
                contacts = paginator.page(paginator.num_pages)

            return contacts


def get_condition(request):
    user = request.user
    user_id = user.id
    cnd = 1

    # if the user has already searched and is now paginating
    if request.method == 'GET':
        cnd = 1

    elif user_id % 2 is 0:
        cnd = 1

    elif user_id % 2 is not 0:
        cnd = 2

    return cnd



