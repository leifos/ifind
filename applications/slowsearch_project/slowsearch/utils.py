__author__ = 'Craig'

import time
from ifind.search import Query, EngineFactory
from logger_practice import event_logger
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from keys import BING_API_KEY

e = EngineFactory("Bing", api_key=BING_API_KEY)  # create Bing search engine object using api key


delay_time = 5  # length of delay for mod_slow in seconds


def mod_normal(results):
    """
    a normal search, no modifications are made

    :param results: the results from the previouly performed search
    :return: (Response)the unchanged results
    """
    return results


def mod_slow(results, delay=delay_time):
    """
    delays the search but leaves the results unchanged

    :param results: the results from the previously performed search
    :param delay: the length of the delay in seconds
    :return: (Response)the unchanged results
    """
    time.sleep(delay)
    return results


# returns 'bad' results
def mod_bad(results):
    """
    does not delay the search, but modifies the results so as to make them worse

    :param results: the results from the previously performed search
    :return: (Response)the results modified to make them 'bad'
    """
    return results


# dictionary of modifier functions
conditions = {
    1: mod_normal,
    2: mod_slow,
    3: mod_bad
}


def run_query(query, condition):
    """
    runs a search query on Bing using the query string passed,
    applies the relevant modifier function and returns the results

    :param query: (str)the query input by the user
    :param condition: (int)the interface condition applied to the user's profile
    :return: (Response)the results of the search after applying the correct modifier function
    """
    q = Query(query, top=100)

    # TODO(leifos): Add some form of caching here
    response = e.search(q)

    mod = conditions[condition]
    mod_results = mod(response)

    return mod_results


def get_condition(request):
    """
    works out the user's condition from their user id

    :param request: (HttpResponse)metadata about the request
    :return: (int)the condition applied to the user account based on their user_id
    """
    user = request.user
    user_id = user.id
    cnd = 1

    # if the user has already searched and is now paginating
    if request.method == 'GET':
        cnd = 1

    elif user_id % 2 == 0:
        cnd = 1

    elif user_id % 2 != 0:
        cnd = 2

    return cnd


def paginated_search(request, query):
    """
    performs a paginated search based on a given query

    :param request: (HttpRequest)the metadata about the request
    :param query: (str)the search query input by the user
    :return: (paginator.Page)paginated results of the search
    """
    cnd = get_condition(request)
    if query:

            event_logger.info('query issued by [' + str(request.user.username)
                              + '], [' + str(len(query)) + '] chars long')

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






