from ifind.search import Query, EngineFactory
from keys import bing_api_key
from models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

bing_engine = EngineFactory("Bing", api_key=bing_api_key)

def mod_normal(results):
    return results

def mod_slow(response):
    return response

def mod_bad(response):
    #returns results in reverse order
    results = response.results
    r = list(results)
    mod_r = r[::-1]
    response.results = mod_r
    return response

conditions = {
    1: mod_normal,
    2: mod_bad,
    3: mod_slow
}

def get_user_condition(request):
    #user = request.user.id
    #profile = UserProfile.objects.get(user)
    #condition = profile.condition
    user_id = request.user.id
    if user_id % 2 is 0:
        condition=1
    elif user_id % 2 is not 0:
        condition=2
    print condition
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
            response = run_query(query, condition)

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

