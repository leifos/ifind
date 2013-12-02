__author__ = 'leif'

import os
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from models import DocumentsExamined
from models import TaskDescription, TopicQuerySuggestion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import simplejson
from django.core.exceptions import ObjectDoesNotExist
from ifind.search import Query, Response

# Whoosh
from whoosh.index import open_dir

# Cache for autocomplete trie
from django.core import cache

# Timing Query
import timeit

# Experiments
from experiment_functions import get_topic_relevant_count
from experiment_functions import get_experiment_context, print_experiment_context
from experiment_functions import mark_document, log_event
from experiment_functions import time_search_experiment_out,getPerformance, getQueryResultPerformance, get_query_performance_metrics
from experiment_configuration import my_whoosh_doc_index_dir
from experiment_configuration import experiment_setups
from time import sleep
from threading import Thread
import json

ix = open_dir(my_whoosh_doc_index_dir)
ixr = ix.reader()

@login_required
def show_document(request, whoosh_docid):
    #check for timeout
    if time_search_experiment_out(request):
        return HttpResponseRedirect('/treconomics/timeout/')

    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    taskid = ec["taskid"]

    condition = ec["condition"]
    current_search = request.session['queryurl']

    # get document from index
    fields = ixr.stored_fields(int(whoosh_docid))
    title = fields["title"]
    content = fields["content"]
    docnum = fields["docid"]
    doc_date = fields["timedate"]
    doc_source = fields["source"]
    docid = whoosh_docid
    topicnum = ec["topicnum"]

    # check if there are any get parameters.
    user_judgement = -2
    rank = 0
    if request.is_ajax():
        getdict = request.GET

        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])

            if 'rank' in getdict:
                rank = int(getdict['rank'])

            #marks that the document has been marked rel or nonrel
            doc_length = ixr.doc_field_length(long(request.GET.get('docid', 0)), 'content')
            user_judgement = mark_document(request, docid, user_judgement, title, docnum, rank, doc_length)
            #mark_document handles logging of this event
        return HttpResponse(simplejson.dumps(user_judgement), mimetype='application/javascript')
    else:
        if time_search_experiment_out( request ):
            return HttpResponseRedirect('/treconomics/next/')
        else:
            #marks that the document has been viewed
            if request.method == 'GET':
                getdict = request.GET
                if 'rank' in getdict:
                    rank = int(getdict['rank'])

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
            #updates the judgement for this document
            doc_length = ixr.doc_field_length(docid, 'content')
            trecid = ixr.stored_fields(docid)['docid']

            user_judgement = mark_document(request=request, whooshid=docid, trecid=trecid, judgement=user_judgement, doc_length=doc_length)

    # Get documents that are for this task, and for this user
    u = User.objects.get(username=uname)
    docs = DocumentsExamined.objects.filter(user=u).filter(task=taskid)
    return render_to_response('trecdo/saved_documents.html', {'participant': uname, 'task': taskid, 'condition': condition, 'current_search': current_search, 'docs': docs}, context)

@login_required
def task(request, taskid):
    print "TASK_SET_TO " +  taskid
    request.session['taskid'] = taskid
    pid = request.user.username
    return HttpResponse(pid + " you're task is set to: "+ taskid +". <a href='/treconomics/saved/'>click here</a>" )

def constructStructuredQuery(request):
    user_and = request.POST['queryAND'].strip()
    user_and1 = request.POST['queryAND1'].strip()
    user_and2 = request.POST['queryAND2'].strip()
    user_and3 = request.POST['queryAND3'].strip()
    user_and4 = request.POST['queryAND4'].strip()

    def buildQueryParts(term_list, op):
        qp = ''
        for t in term_list:
            if t:
                if qp:
                    qp = qp + " "+ op  +" " + t
                else:
                    qp = t
        return qp

    def buildQueryPartsNot(term_list):
        qp = ''
        for t in term_list:
            if t:
                nt = " NOT " + t
                qp = qp + nt
        return qp

    query_and = buildQueryParts([user_and, user_and1, user_and2, user_and3, user_and4], "AND" )
    #print "AND-Query: " + query_and
    user_or = request.POST['queryANY'].strip()
    user_or1 = request.POST['queryANY1'].strip()
    user_or2 = request.POST['queryANY2'].strip()
    user_or3 = request.POST['queryANY3'].strip()
    user_or4 = request.POST['queryANY4'].strip()

    query_or = buildQueryParts([user_or,user_or1,user_or2,user_or3,user_or4], "OR")

    #print "OR-Query: " +  query_or

    user_not = request.POST['queryNOT'].strip()
    user_not1 = request.POST['queryNOT1'].strip()
    user_not2 = request.POST['queryNOT2'].strip()
    user_not3 = request.POST['queryNOT3'].strip()
    user_not4 = request.POST['queryNOT4'].strip()

    query_not = buildQueryPartsNot([user_not,user_not1,user_not2,user_not3,user_not4])
    #print "Not-Query: " +  query_not

    if query_and:
     user_query = query_and

    if query_or:
     if user_query:
         user_query = user_query + " AND ( " + query_or + " ) "
     else:
         user_query = query_or

    if user_not:
     if user_query:
         user_query = user_query + " AND ( " + query_not + " ) "
     else:
         user_query = query_not

    #print user_query
    #user_query = user_and + ' ' + user_or + ' ' + user_not
    user_query = user_query.strip()
    return user_query


def run_query(request, result_dict={}, query_terms='', page=1, page_len=10, condition=0, log_performance=False):
    # Stops an AWFUL lot of problems when people get up to mischief
    if page < 1:
        page = 1

    ec = get_experiment_context(request)

    query = Query(query_terms)
    query.skip = page
    query.top = page_len

    result_dict['query'] = query_terms
    search_engine = experiment_setups[condition].get_engine()
    response = search_engine.search(query)

    num_pages = response.total_pages

    result_dict['trec_results'] = None
    result_dict['trec_no_results_found'] = True
    result_dict['trec_search'] = False
    result_dict['num_pages'] = num_pages

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

    # Disable performance logging - it's a hogging the performance!
    # If log_performance is True, we log the performance metrics.
    #if log_performance:
    #    log_event(event="QUERY_PERF",
    #              request=request,
    #              query=query_terms,
    #              metrics=get_query_performance_metrics(result_dict['trec_results'], ec['topicnum']))

    return result_dict

@login_required
def search(request, taskid=-1):

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

    #check for timeout
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
        interface = experiment_setups[condition].get_interface()
        page_len = experiment_setups[condition].rpp
        page = 1

        result_dict = {}
        result_dict['participant'] = uname
        result_dict['task'] = taskid
        result_dict['condition'] = condition
        result_dict['interface'] = interface
        result_dict['application_root'] = '/treconomics/'
        result_dict['ajax_search_url'] = 'searcha/'
        result_dict['autocomplete'] = experiment_setups[condition].autocomplete

        # Ensure that we set a queryurl.
        # This means that if a user clicks "View Saved" before posing a query, there will be something
        # to go back to!
        if not request.session.get('queryurl'):
            queryurl = result_dict['application_root'] + 'search/'
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl

        suggestions = False
        query_flag = False
        if request.method =='POST':
            # handle the searches from the different interfaces
            if interface == 1:
                user_query = constructStructuredQuery(request)
            else:
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
                result_dict = get_results(request,
                                          page,
                                          page_len,
                                          condition,
                                          user_query,
                                          request.GET.get('noperf'),
                                          experiment_setups[ec['condition']].engine)

                result_dict['participant'] = uname
                result_dict['task'] = taskid
                result_dict['condition'] = condition
                result_dict['interface'] = interface
                result_dict['application_root'] = '/treconomics/'
                result_dict['ajax_search_url'] = 'searcha/'
                result_dict['autocomplete'] = experiment_setups[condition].autocomplete
                result_dict['page'] = page

                if interface == 3:
                        # getQuerySuggestions(topic_num)
                        suggestions = TopicQuerySuggestion.objects.filter(topic_num=topic_num)
                        if suggestions:
                            result_dict['query_suggest_search'] = True
                            entries = []
                            for s in suggestions:
                                entries.append({'title': s.title, 'link': s.link})
                            print entries
                            result_dict['query_suggest_results'] = entries
                        # addSuggestions to results dictionary

                if result_dict['trec_results']:
                    qrp = getQueryResultPerformance(result_dict['trec_results'], topic_num)
                    log_event(event='SEARCH_RESULTS_PAGE_QUALITY',
                              request=request,
                              whooshid=page,
                              rank=qrp[0],
                              judgement=qrp[1])

                result_dict['delay_results'] = experiment_setups[condition].delay_results

                queryurl = '/treconomics/search/?query=' + user_query.replace(' ', '+') + '&page=' + str(page) + '&noperf=true'
                print "Set queryurl to : " + queryurl
                request.session['queryurl'] = queryurl

                result_dict['display_query'] = result_dict['query']

                if len(result_dict['query']) > 50:
                    result_dict['display_query'] = result_dict['query'][0:50] + '...'

                print "Delay time - query execution time: {0}".format(experiment_setups[condition].delay_results - result_dict['query_time'])

                if experiment_setups[condition].delay_results > 0 and (experiment_setups[condition].delay_results - result_dict['query_time'] > 0) and is_from_search_request(page):
                    log_event(event='DELAY_RESULTS_PAGE', request=request, page=page)
                    sleep(experiment_setups[condition].delay_results - result_dict['query_time'])  # Delay search results.

                log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
                return render_to_response('trecdo/results.html', result_dict, context)
        else:
            log_event(event='VIEW_SEARCH_BOX', request=request, page=page)
            result_dict['delay_results'] = experiment_setups[condition].delay_results
            return render_to_response('trecdo/search.html', result_dict, context)


def get_results(request, page, page_len, condition, user_query, prevent_performance_logging, engine):
    """
    Returns a results dictionary object for the given parameters above.
    If the combinations have been previously used, we return a cached version (if it still exists).
    If a cached version does not exist, we query Whoosh and return the results.
    """
    def get_cache_key(page_no, query_terms, engine):
        """
        Nested function to return a unique key for a given combination of inputs.
        The returned string is used as a key value for the cache so results can be stored and retrieved.
        """
        no_space_terms = query_terms.replace(' ', '_')
        return "key-{0}-{1}-{2}".format(engine.get_setup_identifier(), page_no, no_space_terms)

    start_time = timeit.default_timer()

    # Check the cache - has it been queried already?
    # If it has, use the stored result. Else, we need to ask Whoosh.
    cache_key = get_cache_key(page, user_query, engine)
    result_cache = cache.get_cache('default')
    result_dict = result_cache.get(cache_key)  # Query the cache...

    # prevent_performance_logging can be passed to override logging.
    # If a user is on page 2 then goes back to page 1, we don't want to get the performance again.
    if not prevent_performance_logging and page == 1:
        print "Performance should be measured - but it's disabled as it's too costly!"
        #print "Spawning thread to obtain performance of query '{0}'".format(user_query)
        #perf_thread = Thread(target=run_query, args=(request, {}, user_query, 1, 500, condition, True))
        #perf_thread.start()

    # If the result_dict is None, the stuff isn't in the cache so we query Whoosh.
    if not result_dict:
        result_dict = {}
        result_dict = run_query(request, result_dict, user_query, page, page_len, condition)
        result_cache.set(cache_key, result_dict, 300)

    result_dict['query_time'] = timeit.default_timer() - start_time
    return result_dict


@login_required
def ajax_search(request, taskid=-1):
    """
    David's crummy AJAX search implementation.
    Actually, it's not that crummy at all.
    """
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

        return HttpResponseRedirect('/treconomics/searcha/')

    # Has the experiment timed out? If so, indicate to the user.
    # Send a JSON object back which will be interpreted by the JavaScript.
    if time_search_experiment_out(request):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')
    else:
        context = RequestContext(request)
        context_dict = {}

        context_dict['ajax_enabled'] = True
        context_dict['application_root'] = '/treconomics/'
        context_dict['ajax_search_url'] = 'searcha/'

        # Ensure that we set a queryurl.
        # This means that if a user clicks "View Saved" before posing a query, there will be something
        # to go back to!
        if not request.session.get('queryurl'):
            queryurl = context_dict['application_root'] + 'searcha/'
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl

        # Gather the usual suspects...
        ec = get_experiment_context(request)
        uname = ec["username"]
        condition = ec["condition"]
        taskid = ec["taskid"]
        topic_num = ec["topicnum"]
        interface = experiment_setups[condition].get_interface()
        page_len = experiment_setups[condition].rpp
        page = 1

        context_dict['participant'] = uname
        context_dict['task'] = taskid
        context_dict['condition'] = condition
        context_dict['interface'] = interface
        context_dict['autocomplete'] = experiment_setups[condition].autocomplete

        if request.method == 'POST':
            # AJAX POST request for a given query.
            # Returns a AJAX response with the document list to populate the container <DIV>.

            # Should we do a delay? This is true when a user navigates back to the results page from elsewhere.
            do_delay = bool(request.POST.get('noDelay'))

            if interface == 1:
                querystring = request.POST.copy()
                del querystring['csrfmiddlewaretoken']
                request.session['last_ajax_interface1_querystring'] = querystring

                user_query = constructStructuredQuery(request)
            else:
                user_query = request.POST.get('query').strip()

            if not do_delay:  # Do not log the query issued event if the user is returning to the results page.
                log_event(event="QUERY_ISSUED", request=request, query=user_query)

            page_request = request.POST.get('page')

            if page_request:
                page = int(page_request)

            if user_query == "":
                # Nothing to query, tell the client.
                return HttpResponse(json.dumps({'no_results': True}), content_type='application/json')
            else:
                # Get some results! Call this wrapper function which uses the Django cache backend.
                result_dict = get_results(request,
                                           page,
                                           page_len,
                                           condition,
                                           user_query,
                                           request.POST.get('noperf'),
                                           experiment_setups[ec['condition']].engine)

                queryurl = context_dict['application_root'] + context_dict['ajax_search_url'] + '#query=' + user_query.replace(' ', '+') + '&page=' + str(page) + '&noperf=true'
                print "Set queryurl to : " + queryurl
                request.session['queryurl'] = queryurl

                print "Delay time - query execution time: {0}".format(experiment_setups[condition].delay_results - result_dict['query_time'])

                if experiment_setups[condition].delay_results > 0 and (experiment_setups[condition].delay_results - result_dict['query_time'] > 0) and not do_delay:
                    log_event(event='DELAY_RESULTS_PAGE', request=request, page=page)
                    sleep(experiment_setups[condition].delay_results - result_dict['query_time'])  # Delay search results.

                result_dict['display_query'] = result_dict['query']

                if len(result_dict['query']) > 50:
                    result_dict['display_query'] = result_dict['query'][0:50] + '...'

                # Serialis(z?)e the data structure and send it back
                if not do_delay:  # Only log the following if the user is not returning back to the results page.
                    log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
                return HttpResponse(json.dumps(result_dict), content_type='application/json')
        else:
            # Render the search template as usual...
            log_event(event="VIEW_SEARCH_BOX", request=request, page=page)
            context_dict['delay_results'] = experiment_setups[condition].delay_results
            return render_to_response('trecdo/search.html', context_dict, context)

@login_required
def ajax_interface1_querystring(request):
    querydict = request.session['last_ajax_interface1_querystring']
    querystring = ""

    for query in querydict:
        querystring += query + '=' + querydict[query] + '&'

    querystring = querystring[0:len(querystring) - 1]

    return HttpResponse(json.dumps({'querystring': querystring}), content_type='application/json')


@login_required
def view_log_query_focus(request):
    context = RequestContext(request)
    log_event(event='QUERY_FOCUS', request=request )
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
        topic_desc = TaskDescription.objects.get( topic_num = t ).title
        perf["title"] = topic_desc
        perf["score"] = ratio(float(perf["rels"]), float(perf["nons"]))
        perf["total"] = get_topic_relevant_count(t)

        performances.append(perf)

    for p in performances:
        print p

    log_event(event="VIEW_PERFORMANCE", request=request)
    return render_to_response('base/performance_experiment.html', {'participant': uname, 'condition': condition, 'performances': performances}, context)

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

    if request.GET.get('suggest'):
        results = []

        if experiment_setups[condition].autocomplete:
            chars = unicode(request.GET.get('suggest'))

            # See if the cache has what we are looking for.
            # If it does, pull it out and use that.
            # If it doesn't, query the trie and store the results in the cache before returning.
            autocomplete_cache = cache.get_cache('autocomplete')
            results = autocomplete_cache.get(chars)

            if not results:
                suggestion_trie = experiment_setups[condition].get_trie()
                results = suggestion_trie.suggest(chars)
                cache_time = 300

                autocomplete_cache.set(chars, results, cache_time)

        response_data = {
            'count': len(results),
            'results': results,
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')

    return HttpResponseBadRequest(json.dumps({'error': True}), content_type='application/json')