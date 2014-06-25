from ifind.search import Query, EngineFactory
from keys import bing_api_key
from models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

bing_engine = EngineFactory("Bing", api_key=bing_api_key)

def mod_normal(results):
    return results

def mod_slow(results):
    return results

def mod_bad(results):
    #returns results in reverse order
    r = list(results)
    mod_r = r[::-1]
    return mod_r

conditions = {
    1: mod_normal,
    2: mod_bad,
    3: mod_slow
}

def get_user_condition(request):
    user = request.user
    profile = UserProfile.objects.get(user)
    condition = profile.condition


    return condition

def run_query(query, condition=1):
    q = Query(query, top=50)
    print query, q
    print bing_engine

    # check cache, if query is there, return results
    # else send query to bing, and store the results in the cache
    response = bing_engine.search(q)
    print response
    mod = conditions[condition]
    mod_results = mod(response)
    #for r in mod_results:
      #  print r

    return mod_results

def paginated_search(request, query):
    #condition = get_user_condition(request)
    #print condition

    if query:
            result_list = run_query(query)

            paginator = Paginator(result_list.results, 10)
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

