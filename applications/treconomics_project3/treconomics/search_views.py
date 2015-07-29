__author__ = 'leif'

import os
import sys
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from models import DocumentsExamined
from models import TaskDescription
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist
from ifind.search import Query
from urllib import urlencode

# Whoosh
from whoosh.index import open_dir

# Cache for autocomplete trie
from django.core import cache

# Timing Query
import timeit

# Experiments
from experiment_functions import get_topic_relevant_count
from experiment_functions import get_experiment_context
from experiment_functions import mark_document, log_event
from experiment_functions import time_search_experiment_out, getPerformance, getQueryResultPerformance, log_performance
from experiment_configuration import my_whoosh_doc_index_dir, data_dir
from experiment_configuration import experiment_setups
from time import sleep
import json

ix = open_dir(my_whoosh_doc_index_dir)
ixr = ix.reader()


@login_required
def show_document(request, whoosh_docid):
    # check for timeout
    """
    Displays the document selected by the user
    :param request:
    :param whoosh_docid: the way of identifying the selected document
    :return:
    """
    sys.stdout.flush()
    if time_search_experiment_out(request):
        return HttpResponseRedirect('/treconomics/timeout/')

    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    taskid = ec["taskid"]

    condition = ec["condition"]
    current_search = request.session['queryurl']

    log_event(event="DOC_CLICKED",
              request=request,
              whooshid=whoosh_docid)

    # get document from index
    fields = ixr.stored_fields(int(whoosh_docid))
    title = fields["title"]
    content = fields["content"]
    docnum = fields["docid"]
    doc_date = fields["timedate"]
    doc_source = fields["source"]
    docid = whoosh_docid
    topicnum = ec["topicnum"]

    def get_document_rank():
        """
        Returns the rank (integer) for the given document ID.
        -1 is returned if the document is not found in the session ranked list.
        """
        the_docid = int(whoosh_docid)
        ranked_results = request.session.get('results_ranked', [])

        # Some list comprehension - returns a list of one integer with the rank of a given document
        # if it exists in ranked_results; returns a blank list if the document is not present.
        at_rank = [item[1] for item in ranked_results if item[0] == the_docid]

        if len(at_rank) > 0:
            return at_rank[0]
        else:
            return -1

    # check if there are any get parameters.
    user_judgement = -2
    rank = 0
    if request.is_ajax():
        getdict = request.GET

        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])
            rank = get_document_rank()

            # marks that the document has been marked rel or nonrel
            doc_length = ixr.doc_field_length(long(request.GET.get('docid', 0)), 'content')
            user_judgement = mark_document(request, docid, user_judgement, title, docnum, rank, doc_length)
            # mark_document handles logging of this event
        return HttpResponse(simplejson.dumps(user_judgement), mimetype='application/javascript')
    else:
        if time_search_experiment_out(request):
            return HttpResponseRedirect('/treconomics/next/')
        else:
            # marks that the document has been viewed
            rank = get_document_rank()

            doc_length = ixr.doc_field_length(long(docid), 'content')
            user_judgement = mark_document(request, docid, user_judgement, title, docnum, rank, doc_length)

            context_dict = {'participant': uname,
                            'task': taskid,
                            'condition': condition,
                            'current_search': current_search,
                            'docid': docid,
                            'docnum': docnum,
                            'title': title,
                            'doc_date': doc_date,
                            'doc_source': doc_source,
                            'content': content,
                            'user_judgement': user_judgement,
                            'rank': rank}

            if request.GET.get('backtoassessment', False):
                context_dict['backtoassessment'] = True

            return render_to_response('trecdo/document.html', context_dict, context)


@login_required
def show_saved_documents(request):
    context = RequestContext(request)

    # Timed out?
    if time_search_experiment_out(request):
        return HttpResponseRedirect('/treconomics/timeout/')

    ec = get_experiment_context(request)
    taskid = ec['taskid']
    condition = ec['condition']
    uname = ec['username']
    current_search = request.session['queryurl']

    user_judgement = -2
    if request.method == 'GET':
        getdict = request.GET

        if 'judge' not in getdict and 'docid' not in getdict:
            # Log only if user is entering the page, not after clicking a relevant button
            print "LOG_VIEW_SAVED_DOCS"
            log_event(event="VIEW_SAVED_DOCS", request=request)

        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])
        if 'docid' in getdict:
            docid = int(getdict['docid'])
        if (user_judgement > -2) and (docid > -1):
            # updates the judgement for this document
            doc_length = ixr.doc_field_length(docid, 'content')
            trecid = ixr.stored_fields(docid)['docid']

            user_judgement = mark_document(request=request, whooshid=docid, trecid=trecid, judgement=user_judgement,
                                           doc_length=doc_length)

    # Get documents that are for this task, and for this user
    u = User.objects.get(username=uname)
    docs = DocumentsExamined.objects.filter(user=u).filter(task=taskid)
    return render_to_response('trecdo/saved_documents.html',
                              {'participant': uname, 'task': taskid, 'condition': condition,
                               'current_search': current_search, 'docs': docs}, context)


@login_required
def task(request, taskid):
    print "TASK_SET_TO " + taskid
    request.session['taskid'] = taskid
    pid = request.user.username
    return HttpResponse(pid + " your task is set to: " + taskid + ". <a href='/treconomics/saved/'>click here</a>")


def reduce_snippet(response, percent):
    for s in response.results:
        print s
        summary = s.summary
        l = len(summary)
        p = l
        if l > 5:
            p = int(float(l) * (percent / 100.0)) + 2
        s.summary = summary[:p]
    return response


def run_query(request, result_dict, query_terms='', page=1, page_len=10, condition=0, interface=1):
    # Stops an AWFUL lot of problems when people get up to mischief
    if page < 1:
        page = 1

    ec = get_experiment_context(request)

    query = Query(query_terms)
    query.skip = page
    query.top = page_len
    result_dict['query'] = query_terms
    search_engine = experiment_setups[condition].get_engine()

    log_event(event="QUERY_START", request=request, query=query_terms)
    response = search_engine.search(query)
    """
    Now that we have the response, we can iterate through it, and modify the snippets
    based on the interface.
    """
    if interface == 1:
        pass
        # no change to length
    if interface == 2:
        # call a method that takes response and process it for interface 1, etc
        response = reduce_snippet(response, 10)

    if interface == 3:
        response = reduce_snippet(response, 50)

    """
    Add in your code here.
    """

    log_event(event="QUERY_END", request=request, query=query_terms)
    num_pages = response.total_pages

    result_dict['trec_results'] = None
    result_dict['trec_no_results_found'] = True
    result_dict['trec_search'] = False
    result_dict['num_pages'] = num_pages

    print "PAGE"
    print num_pages

    if num_pages > 0:
        result_dict['trec_search'] = True
        result_dict['trec_results'] = response.results

        result_dict['curr_page'] = response.actual_page
        if page > 1:
            result_dict['prev_page'] = page - 1
            result_dict['prev_page_show'] = True

            if (page - 1) == 1:
                result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=1&noperf=true'
            else:
                result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page - 1)
        if page < num_pages:
            result_dict['next_page'] = page + 1
            result_dict['next_page_show'] = True
            result_dict['next_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page + 1)


def get_results(request, result_dict, page, page_len, condition, user_query, interface):
    """
    Returns a results dictionary object for the given parameters above.
    If the combinations have been previously used, we return a cached version (if it still exists).
    If a cached version does not exist, we query Whoosh and return the results.
    """

    start_time = timeit.default_timer()
    # prevent_performance_logging can be passed to override logging.
    # If a user is on page 2 then goes back to page 1, we don't want to get the performance again.
    # if not prevent_performance_logging and page == 1:
    # print "Performance should be measured - but it's disabled as it's too costly!"

    run_query(request, result_dict, user_query, page, page_len, condition, interface)
    result_dict['query_time'] = timeit.default_timer() - start_time


def set_task(request, taskid=-1):
    if isinstance(taskid, unicode):
        taskid = int(taskid)

    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 0:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid

        if taskid == 0:
            log_event(event="PRACTICE_SEARCH_TASK_COMMENCED", request=request)
        else:
            log_event(event="SEARCH_TASK_COMMENCED", request=request)


@login_required
def search(request, taskid=-1):
    sys.stdout.flush()

    def is_from_search_request(new_page_no):
        """
        Returns True iif the URL of the referer is a standard search request.
        This is used to determine if we should delay results appearing.

        The new page number of required to check against the page number from the referer.
        If they match, we don't delay - if they don't, we do.
        """
        http_referer = request.META['HTTP_REFERER']
        http_referer = http_referer.strip().split('&')
        page = 1

        for item in http_referer:
            if 'page=' in item:
                item = item.split('=')
                page = int(item[1])

        if request.POST.get('newquery') == 'true':
            return '/treconomics/search/' in request.META['HTTP_REFERER']

        return '/treconomics/search/' in request.META['HTTP_REFERER'] and new_page_no == page

    if isinstance(taskid, unicode):
        taskid = int(taskid)

    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 0:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid

        if taskid == 0:
            log_event(event="PRACTICE_SEARCH_TASK_COMMENCED", request=request)
        else:
            log_event(event="SEARCH_TASK_COMMENCED", request=request)

    # check for timeout
    if time_search_experiment_out(request):
        return HttpResponseRedirect('/treconomics/timeout/')
    else:
        """show base index view"""
        context = RequestContext(request)
        ec = get_experiment_context(request)

        uname = ec["username"]
        condition = ec["condition"]
        taskid = ec["taskid"]
        topic_num = ec["topicnum"]
        rotation = ec["rotation"]
        es = experiment_setups[condition]
        exp = es.get_exp_dict(taskid, rotation)
        interface = exp['interface']
        page_len = exp['rpp']
        page = 1

        def setup_result_dict(uname, taskid, condition, interface, experiment, topic_num):
            result_dict = {}
            result_dict['participant'] = uname
            result_dict['task'] = taskid
            result_dict['topicno'] = topic_num
            result_dict['condition'] = condition
            result_dict['interface'] = interface
            result_dict['application_root'] = '/treconomics/'
            result_dict['ajax_search_url'] = 'searcha/'
            result_dict['autocomplete'] = experiment['autocomplete']
            result_dict['is_fast'] = 'true'
            result_dict['delay_results'] = exp['result_delay']
            result_dict['delay_docview'] = exp['docview_delay']
            if experiment['result_delay'] == 0:
                result_dict['is_fast'] = 'false'
            return result_dict


        result_dict = setup_result_dict(uname, taskid, condition, interface, exp, topic_num)

        # Ensure that we set a queryurl.
        # This means that if a user clicks "View Saved" before posing a query, there will be something
        # to go back to!
        if not request.session.get('queryurl'):
            queryurl = result_dict['application_root'] + 'search/'
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl

        suggestions = False
        query_flag = False
        if request.method == 'POST':
            # handle the searches from the different interfaces
            user_query = request.POST['query'].strip()
            log_event(event="QUERY_ISSUED", request=request, query=user_query)
            query_flag = True
            result_dict['page'] = page
        elif request.method == 'GET':
            getdict = request.GET
            if 'query' in getdict:
                user_query = getdict['query']
                query_flag = True
            if 'suggestion' in getdict:
                suggestions = True
            if suggestions:
                log_event(event="QUERY_SUGGESTION_ISSUED", request=request, query=user_query)

            if 'page' in getdict:
                page = int(getdict['page'])
            else:
                page = 1

        if query_flag:
            # If the user poses a blank query, we just send back a results page saying so.
            if user_query == '':
                result_dict['blank_query'] = True
                return render_to_response('trecdo/results.html', result_dict, context)
            else:
                # Get some results! Call this wrapper function which uses the Django cache backend.
                get_results(request, result_dict,
                            page,
                            page_len,
                            condition,
                            user_query,
                            interface)

                result_dict['page'] = page
                result_dict['focus_querybox'] = 'false'

                if result_dict['trec_results'] is None:
                    result_dict['focus_querybox'] = 'true'

                if result_dict['trec_results']:
                    qrp = getQueryResultPerformance(result_dict['trec_results'], topic_num)
                    log_event(event='SEARCH_RESULTS_PAGE_QUALITY',
                              request=request,
                              whooshid=page,
                              rank=qrp[0],
                              judgement=qrp[1])

                query_params = urlencode({'query': user_query, 'page': page, 'noperf': 'true'})
                queryurl = '/treconomics/search/?' + query_params
                print "Set queryurl to : " + queryurl
                request.session['queryurl'] = queryurl

                result_dict['display_query'] = result_dict['query']
                if len(result_dict['query']) > 50:
                    result_dict['display_query'] = result_dict['query'][0:50] + '...'

                if exp['result_delay'] > 0 and is_from_search_request(page):
                    log_event(event='DELAY_RESULTS_PAGE', request=request, page=page)
                    sleep(exp['result_delay'])

                set_results_session_var(request, result_dict)

                log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
                request.session['last_request_time'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
                return render_to_response('trecdo/results.html', result_dict, context)
        else:
            log_event(event='VIEW_SEARCH_BOX', request=request, page=page)
            return render_to_response('trecdo/search.html', result_dict, context)


@login_required
def set_results_session_var(request, result_dict):
    """
    A helper function which sets a session variable containing the Whoosh document IDs for a given
    response.
    """
    results_ranked = []

    if not result_dict['trec_results'] is None:
        for result in result_dict['trec_results']:
            results_ranked.append((result.whooshid, result.rank))

    request.session['results_ranked'] = results_ranked


@login_required
def view_log_query_focus(request):
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    context = RequestContext(request)
    log_event(event='QUERY_FOCUS', request=request)
    return HttpResponse(1)


@login_required
def view_performance(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    rotation = ec["rotation"]

    def ratio(rels, nonrels):
        """ expect two floats
        """
        dem = rels + nonrels
        if dem > 0.0:
            return round((rels * rels) / dem, 2)
        else:
            return 0.0

    topics = experiment_setups[condition].topics

    performances = []
    for t in topics:
        perf = getPerformance(uname, t)
        topic_desc = TaskDescription.objects.get(topic_num=t).title
        perf["num"] = t
        perf["title"] = topic_desc
        perf["score"] = ratio(float(perf["rels"]), float(perf["nons"]))
        perf["total"] = get_topic_relevant_count(t)

        # Should log the performance of each topic here.
        log_performance(request, perf)
        performances.append(perf)

    for p in performances:
        print p

    return render_to_response('base/performance_experiment.html',
                              {'participant': uname, 'condition': condition, 'performances': performances}, context)


@login_required
def view_log_hover(request):
    """
    View which logs a user hovering over a search result.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    ec = get_experiment_context(request)

    uname = ec['username']
    taskid = ec['taskid']
    u = User.objects.get(username=uname)

    status = request.GET.get('status')
    rank = request.GET.get('rank')
    page = request.GET.get('page')
    trec_id = request.GET.get('trecID')
    whoosh_id = request.GET.get('whooshID')
    doc_length = ixr.doc_field_length(long(whoosh_id), 'content')

    try:
        examined = DocumentsExamined.objects.get(user=u, task=taskid, doc_num=trec_id)
        judgement = examined.judgement
    except ObjectDoesNotExist:
        judgement = -2

    if status == 'in':
        log_event(event="DOCUMENT_HOVER_IN",
                  request=request,
                  whooshid=whoosh_id,
                  trecid=trec_id,
                  rank=rank,
                  page=page,
                  judgement=judgement,
                  doc_length=doc_length)
    elif status == 'out':
        log_event(event="DOCUMENT_HOVER_OUT",
                  request=request,
                  whooshid=whoosh_id,
                  trecid=trec_id,
                  rank=rank,
                  page=page,
                  judgement=judgement,
                  doc_length=doc_length)

    return HttpResponse(json.dumps({'logged': True}), content_type='application/json')


@login_required
def suggestion_selected(request):
    """
    Called when a suggestion is selected from the suggestion interface.
    Logs the suggestion being selected.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    new_query = request.GET.get('new_query')
    log_event(event='AUTOCOMPLETE_QUERY_SELECTED', query=new_query, request=request)
    return HttpResponse(json.dumps({'logged': True}), content_type='application/json')


@login_required
def suggestion_hover(request):
    """
    Called when a user hovers over a query suggestion.
    """
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    suggestion = request.GET.get('suggestion')
    rank = int(request.GET.get('rank'))

    log_event(event='AUTOCOMPLETE_QUERY_HOVER', query=suggestion, rank=rank, request=request)
    return HttpResponse(json.dumps({'logged': True}), content_type='application/json')


@login_required
def autocomplete_suggestion(request):
    """
    Handles the autocomplete suggestion service.
    """
    # Get the condition from the user's experiment context.
    # This will yield us access to the autocomplete trie!
    ec = get_experiment_context(request)
    condition = ec['condition']
    rotation = ec['rotation']
    taskid = ec['taskid']
    es = experiment_setups[condition]
    exp = es.get_exp_dict(taskid, rotation)

    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    if request.GET.get('suggest'):
        results = []

        if exp['autocomplete']:
            chars = unicode(request.GET.get('suggest'))

            # See if the cache has what we are looking for.
            # If it does, pull it out and use that.
            # If it doesn't, query the trie and store the results in the cache before returning.
            autocomplete_cache = cache.get_cache('autocomplete')
            results = autocomplete_cache.get(chars)

            if not results:
                suggestion_trie = exp['trie']
                results = suggestion_trie.suggest(chars)
                cache_time = 300

                autocomplete_cache.set(chars, results, cache_time)

        response_data = {
            'count': len(results),
            'results': results,
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponseBadRequest(json.dumps({'error': True}), content_type='application/json')


def view_run_queries(request, topic_num):
    from experiment_configuration import bm25

    context = RequestContext(request)
    num = 0
    query_file_name = os.path.join(data_dir, topic_num + '.queries')
    print query_file_name

    start_time = timeit.default_timer()
    query_list = []

    try:
        query_file = open(query_file_name, "r")
        while query_file and num < 200:
            num += 1
            line = query_file.readline()
            # print line
            parts = line.partition(' ')
            # print parts
            query_num = parts[0]
            query_str = unicode(parts[2])
            if query_str:
                print query_str
                q = Query(query_str)
                q.skip = 1
                response = bm25.search(q)
                query_list.append(query_str)
            else:
                break
    except:
        pass

    seconds = timeit.default_timer() - start_time

    return render_to_response('base/query_test.html', {'topic_num': topic_num, 'seconds': seconds, 'num': num}, context)
