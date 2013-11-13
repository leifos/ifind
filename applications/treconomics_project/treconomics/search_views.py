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
from ifind.search import Query, Response

# Whoosh
from whoosh.index import open_dir

# Experiments
from experiment_functions import get_experiment_context, print_experiment_context
from experiment_functions import mark_document, log_event
from experiment_functions import time_search_experiment_out, getPerformance, getQueryResultPerformance
from experiment_configuration import my_whoosh_doc_index_dir
from experiment_configuration import experiment_setups
from time import sleep
import json

ix = open_dir(my_whoosh_doc_index_dir)
ixr = ix.reader()

@login_required
def show_document(request, whoosh_docid):
    #check for timeout
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
            return render_to_response('trecdo/document.html', {'participant': uname, 'task': taskid, 'condition': condition, 'current_search': current_search, 'docid': docid, 'docnum': docnum, 'title': title, 'doc_date': doc_date,   'doc_source': doc_source, 'content': content, 'user_judgement': user_judgement, 'rank': rank}, context)

@login_required
def show_saved_documents(request):
    #write_to_log("VIEW_SAVED_DOCS" )
    context = RequestContext(request)
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


def run_query(condition=0, result_dict={}, query_terms='', page=1, page_len=10):

    # Stops an AWFUL lot of problems when people get up to mischief
    if page < 1:
        page = 1

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
            result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page - 1)
        if page < num_pages:
            result_dict['next_page'] = page + 1
            result_dict['next_page_show'] = True
            result_dict['next_page_link'] = "?query=" + query_terms.replace(' ', '+') + '&page=' + str(page + 1)

    return result_dict

@login_required
def search(request, taskid=0):

    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 1:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid
        log_event(event="SEARCH_TASK_COMMENCED",request=request)
     #check for timeout
    if time_search_experiment_out( request ) :
        return HttpResponseRedirect('/treconomics/next/')
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

            result_dict['page'] = page

        if query_flag:
            result_dict = run_query(condition, result_dict, user_query, page, page_len)
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

            queryurl = '/treconomics/search/?query=' + user_query.replace(' ', '+') + '&page=' + str(page)
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl
            log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
            return render_to_response('trecdo/results.html', result_dict, context)
        else:
            log_event(event='VIEW_SEARCH_BOX', request=request, page=page)
            return render_to_response('trecdo/search.html', result_dict, context)

@login_required
def ajax_search(request, taskid=0):
    """
    David's crummy AJAX search implementation.
    Actually, it's not that crummy at all.
    """
    # If taskid is set, then it marks the start of a new search task
    # Update the session variable to reflect this
    if taskid >= 1:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = taskid
        log_event(event="SEARCH_TASK_COMMENCED", request=request)
    if taskid == 0:
        request.session['start_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['taskid'] = 0
        log_event(event="PRACTICE_SEARCH_TASK_COMMENCED", request=request)

    # Has the experiment timed out? If so, indicate to the user.
    # Send a JSON object back which will be interpreted by the JavaScript.
    if time_search_experiment_out(request):
        return HttpResponse(json.dumps({'timeout': True}), content_type='application/json')
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
            queryurl = context_dict['application_root'] + 'ajax_search/'
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
            result_dict = {}

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

            result_dict = run_query(condition, result_dict, user_query, page, page_len)

            queryurl = context_dict['application_root'] + context_dict['ajax_search_url'] + '#query=' + user_query.replace(' ', '+') + '&page=' + str(page)
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl

            if experiment_setups[condition].delay_results > 0 and not do_delay:
                log_event(event='DELAY_RESULTS_PAGE', request=request, page=page)
                sleep(experiment_setups[condition].delay_results)  # Delay search results.

            # Serialis(z?)e the data structure and send it back
            if not do_delay:  # Only log the following if the user is not returning back to the results page.
                log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page)
            return HttpResponse(json.dumps(result_dict), content_type='application/json')
        else:
            # Render the search template as usual...
            log_event(event="VIEW_SEARCH_BOX", request=request, page=page)
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
            return round((rels * rels) / dem ,2)
        else:
            return 0.0

    topics = experiment_setups[condition].topics

    performances = []
    for t in topics:
        perf = getPerformance(uname, t)
        topic_desc =  TaskDescription.objects.get( topic_num = t ).title
        perf["title"] = topic_desc
        perf["score"] =  ratio(float(perf["rels"]), float(perf["nons"]))

        performances.append(perf)

    for p in performances:
        print p

    return render_to_response('base/performance_experiment.html', {'participant': uname, 'condition': condition, 'performances': performances }, context)

@login_required
def view_log_hover(request):
    """
    View which logs a user hovering over a search result.
    """
    status = request.GET.get('status')
    rank = request.GET.get('rank')
    page = request.GET.get('page')
    trec_id = request.GET.get('trecID')
    whoosh_id = request.GET.get('whooshID')
    doc_length = ixr.doc_field_length(long(whoosh_id), 'content')

    if status == 'in':
        log_event(event="DOCUMENT_HOVER_IN",
                  request=request,
                  whooshid=whoosh_id,
                  trecid=trec_id,
                  rank=rank,
                  page=page,
                  doc_length=doc_length)
    elif status == 'out':
        log_event(event="DOCUMENT_HOVER_OUT",
                  request=request,
                  whooshid=whoosh_id,
                  trecid=trec_id,
                  rank=rank,
                  page=page,
                  doc_length=doc_length)

    return HttpResponse(json.dumps({'logged': True}), content_type='application/json')

@login_required
def suggestion_selected(request):
    """
    Called when a suggestion is selected from the suggestion interface.
    Logs the suggestion being selected.
    """

    new_query = request.GET.get('new_query')

    log_event(event='AUTOCOMPLETE_QUERY_SELECTED', query=new_query, request=request)
    return HttpResponse(json.dumps({'logged': True}), content_type='application/json')

@login_required
def autocomplete_suggestion(request):
    """
    Handles the autocomplete suggestion service.
    """
    # Get the condition from the user's experiment context.
    # This will yield us access to the autocomplete trie!
    ec = get_experiment_context(request)
    condition = ec["condition"]

    if time_search_experiment_out(request):
        return HttpResponseBadRequest(json.dumps({'timeout': True}), content_type='application/json')

    if request.GET.get('suggest'):
        results = []
        if experiment_setups[condition].autocomplete:
            suggestion_trie = experiment_setups[condition].get_trie()
            # A querystring for suggestions has been supplied; so we return a JSON object with suggestions.
            chars = unicode(request.GET.get('suggest'))
            results = suggestion_trie.suggest(chars)

        response_data = {
            'count': len(results),
            'results': results,
        }

        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponseBadRequest(json.dumps({'error': True}), content_type='application/json')