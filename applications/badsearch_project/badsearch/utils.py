from ifind.search import Query, EngineFactory
from keys import BING_API_KEY
from models import UserProfile
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "badsearch_project.settings")
from django.core.cache import cache, get_cache
import time, datetime
from logger_practice import event_logger
from models import QueryTime, LinkTime
from datetime import timedelta
import hashlib
import pickle

bing_engine = EngineFactory("Bing", api_key=BING_API_KEY)
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
    print condition
    return condition

def get_user_id(request):
    user_id = request.user.id
    return user_id

def run_query(query, condition):
    q = Query(query, top=50)

    # check cache, if query is there, return results
    # else send query to bing, and store the results in the cache
    response = bing_engine.search(q)
    mod = conditions[condition]
    mod_response = mod(response)

    return mod_response

def paginated_search(request, query, user):
    condition = get_user_condition(request)
    user_id = str(user.id)
    q_len = str(len(query))
    page = request.REQUEST.get('page')
    hq = hashlib.sha1(query)
    hash_q = hq.hexdigest()

    if query:

            if not response_cache.get(query):
                response = run_query(query, condition)
                response_cache.set(query, pickle.dumps(response), 600)
                profile = UserProfile.objects.get(user=user)
                query_num = int(profile.num_query)
                profile.num_query = query_num + 1
                profile.save()
                event_logger.info(user_id + ' QL ' + q_len + ' HQ ' + hash_q + ' CA ')

            else:
                response = pickle.loads(response_cache.get(query))
                event_logger.info(user_id + ' HQ ' + hash_q + ' PA ' + str(page) + ' RR')

            paginator = Paginator(response.results, 10)

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                # if page not an integer, deliver first page
                results = paginator.page(1)
            except EmptyPage:
                # if page out of range, deliver last page of results
                results = paginator.page(paginator.num_pages)

            return results

def record_query(user, now):

    user = user
    str_u_ID = str(user.id)

    try:
        qt_obj = QueryTime.objects.get(user=user)
    except QueryTime.DoesNotExist:
        qt_obj = QueryTime.objects.create(user=user, last_query_time=now)

    last_query = QueryTime.objects.get(user=user).last_query_time.replace(tzinfo=None, microsecond=0)

    time = now - last_query - timedelta(hours=1)

    qt_obj.last_query_time = now
    qt_obj.save()

    if time <= timedelta(seconds=0):
        event_logger.info(str_u_ID + ' 1Q')

    elif time < timedelta(minutes=10):
        event_logger.info(str_u_ID + ' RP ' + str(time))

    elif time < timedelta(hours=1):
        event_logger.info(str_u_ID + ' TO')

    else:
        event_logger.info(str_u_ID + ' S1')

def record_link(user, now, url, rank):

    user = user
    str_u_ID = str(user.id)
    hl = hashlib.sha1(url)
    url_visited = hl.hexdigest()
    url_rank = str(rank)

    profile = UserProfile.objects.get(user=user)
    link_num = int(profile.num_links)
    profile.num_links = link_num + 1
    profile.save()

    try:
        lt_obj = LinkTime.objects.get(user=user)
    except LinkTime.DoesNotExist:
        lt_obj = LinkTime.objects.create(user=user, last_link_time=now)

    last_link = LinkTime.objects.get(user=user).last_link_time.replace(tzinfo=None, microsecond=0)

    time = now - last_link - timedelta(hours=1)

    lt_obj.last_link_time = now
    lt_obj.save()

    if time <= timedelta(seconds=0):
        event_logger.info(str_u_ID + ' LV ' + url_visited + ' LR ' + url_rank + ' 1L')

    elif time < timedelta(minutes=10):
        event_logger.info(str_u_ID + ' LV ' + url_visited + ' LR ' + url_rank + ' LT ' + str(time))

    elif time < timedelta(hours=1):
        event_logger.info(str_u_ID + ' LV ' + url_visited + ' LR ' + url_rank + ' TO')

    else:
        event_logger.info(str_u_ID + ' LV ' + url_visited + ' LR ' + url_rank + ' S1')