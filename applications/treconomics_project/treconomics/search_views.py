__author__ = 'leif'

import os
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import DocumentsExamined
from models import TaskDescription, TopicQuerySuggestion
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import simplejson

from ifind.search.engines.whooshtrecnews import WhooshTrecNews
from ifind.search import Query, Response

# Whoosh
from whoosh.index import open_dir

# PuppyIR
#from puppy.model import Query, Response

# Service
#from service import service

# Experiments
from experiment_functions import get_experiment_context, print_experiment_context
from experiment_functions import mark_document, log_event
from experiment_functions import time_search_experiment_out, getPerformance, ReadQrelsFile
from experiment_configuration import my_whoosh_doc_index_dir, qrels_file
from experiment_configuration import experiment_setups

ix = open_dir(my_whoosh_doc_index_dir)
ixr = ix.reader()

print "creating search engine"
search_engine = WhooshTrecNews(whoosh_index_dir=my_whoosh_doc_index_dir)


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
    fields = ixr.stored_fields( int(whoosh_docid) )
    title = fields["title"]
    content = fields["content"]
    docnum = fields["docid"]
    doc_date = fields["timedate"]
    doc_source = fields["source"]
    docid = whoosh_docid
    topicnum = ec["topicnum"]
    print docid
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
            user_judgement = mark_document(request, docid, user_judgement, title, docnum, rank)
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
            user_judgement = mark_document(request, docid, user_judgement, title, docnum, rank)
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

    print "LOG_VIEW_SAVED_DOCS"
    log_event(event="VIEW_SAVED_DOCS", request=request)

    user_judgement = -2
    if request.method == 'GET':
        getdict = request.GET
        if 'judge' in getdict:
            user_judgement = int(getdict['judge'])
        if 'doc' in getdict:
            docid = int(getdict['doc'])
        if (user_judgement > -2) and (docid > -1):
            #updates the judgement for this document
            user_judgement = mark_document(request=request, docid=docid, judgement=user_judgement)

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
         user_query = user_query + " AND " + query_or
     else:
         user_query = query_or

    if user_not:
     if user_query:
         user_query = user_query + " AND " + query_not
     else:
         user_query = query_not

    #print user_query
    #user_query = user_and + ' ' + user_or + ' ' + user_not
    user_query = user_query.strip()
    return user_query


def run_query(condition=0, result_dict={}, query_terms='', page=1):

    page_len = experiment_setups[condition].rpp

    query = Query(query_terms)
    query.skip = page
    query.top = page_len

    result_dict['query'] = query_terms
    response = search_engine.search(query)

    num_pages = response.result_total

    if num_pages > 0:
        result_dict['trec_search'] = True
        result_dict['trec_results'] = response.results

        result_dict['curr_page'] = page
        if page > 1:
            result_dict['prev_page'] = page - 1
            result_dict['prev_page_show'] = True
            result_dict['prev_page_link'] = "?query=" + query_terms.replace(' ','+') + '&page=' + str(page - 1)
        if page < num_pages:
            result_dict['next_page'] = page + 1
            result_dict['next_page_show'] = True
            result_dict['next_page_link'] = "?query=" + query_terms.replace(' ','+') + '&page=' + str(page + 1)
            result_dict['num_pages'] = num_pages
    else:
        result_dict['trec_no_results_found'] = True

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

        result_dict = {}
        result_dict['participant'] = uname
        result_dict['task'] = taskid
        result_dict['condition'] = condition

        suggestions = False
        query_flag = False
        if request.method =='POST':
            # handle the searches from the different interfaces
            if condition == 1:
                user_query = constructStructuredQuery(request)
            else:
                user_query = request.POST['query'].strip()
            log_event(event="QUERY_ISSUED", request=request, query=user_query)

            query_flag = True
            page = 1
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
            """
            query = Query(user_query)
            query.start_page = page
            query.page_len = 10
            if condition == 4:
                query.page_len = 3
            if condition == 5:
                query.page_len = 6
            #check if trec_search exists, if so, include web results
            result_dict['query'] = user_query

            if 'trec_search' in service.search_services:
                print "trec_search service included"
                trec_results = service.search_services['trec_search'].search(query)
                if trec_results.get_totalresults > 0:
                    result_dict['trec_search'] = True
                    result_dict['trec_results'] = trec_results.entries
                    #curr_page = page
                    #num_pages = 100
                    # THIS NEEDS TO BE FIXED - problem with calls to get_startindex() and get_totalresults()
                    curr_page = trec_results.get_startindex()
                    num_pages = trec_results.get_totalresults()
                    #print "THIS IS: " + str(curr_page)
                    result_dict['curr_page'] = curr_page
                    if curr_page > 1:
                        result_dict['prev_page'] = curr_page - 1
                        result_dict['prev_page_show'] = True
                        result_dict['prev_page_link'] = "?query=" + user_query.replace(' ','+') + '&page=' + str(curr_page - 1)
                    if curr_page < num_pages:
                        result_dict['next_page'] = curr_page + 1
                        result_dict['next_page_show'] = True
                        result_dict['next_page_link'] = "?query=" + user_query.replace(' ','+') + '&page=' + str(curr_page + 1)
                    result_dict['num_pages'] = num_pages
                else:
                    result_dict['trec_no_results_found'] = True
            """
            result_dict = run_query(condition,result_dict,user_query,page)


            # check the condition
            # check if query_suggest_search exists, if so include query_results
            if condition == 3:
                    topic_num = ec["topicnum"]
                    # getQuerySuggestions(topic_num)
                    suggestions = TopicQuerySuggestion.objects.filter(topic_num = topic_num)
                    if suggestions:
                        result_dict['query_suggest_search'] = True
                        entries = []
                        for s in suggestions:
                            entries.append({'title': s.title, 'link': s.link})
                        print entries
                        result_dict['query_suggest_results'] = entries
                    # addSuggestions to results dictionary


            queryurl = '/treconomics/search/?query=' + user_query.replace(' ','+') + '&page=' + str(page)
            print "Set queryurl to : " + queryurl
            request.session['queryurl'] = queryurl
            log_event(event='VIEW_SEARCH_RESULTS_PAGE', request=request, page=page )
            return render_to_response('trecdo/results.html', result_dict, context)
        else:
            log_event(event='VIEW_SEARCH_BOX', request=request, page=page )
            return render_to_response('trecdo/search.html', result_dict, context)


@login_required
def view_performance(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    rotation = ec["rotation"]

    qrels = ReadQrelsFile( qrels_file )

    task1 = getPerformance(qrels, uname, 1, rotation)
    t = TaskDescription.objects.get( topic_num = task1['topicnum'] )
    task1["title"] = t.title

    dem = float(task1["rels"] + task1["nons"])
    if dem > 0.0:
        task1["score"] = round(float(task1["rels"] * task1["rels"] ) / dem ,2)
    else:
        task1["score"] = 0.0

    task2 = getPerformance(qrels, uname, 2, rotation)
    t = TaskDescription.objects.get( topic_num = task2['topicnum'] )
    task2["title"] = t.title

    dem = float(task2["rels"] + task2["nons"])
    if dem > 0.0:
        task2["score"] = round(float(task2["rels"] * task2["rels"] ) / dem ,2)
    else:
        task2["score"] = 0.0

    task3 = getPerformance(qrels, uname, 3, rotation)
    t = TaskDescription.objects.get( topic_num = task3['topicnum'] )
    task3["title"] = t.title
    dem = float(task3["rels"] + task3["nons"])
    if dem > 0.0:
        task3["score"] = round(float(task3["rels"] * task3["rels"] ) / dem,2)
    else:
        task3["score"] = 0

    print task1["rels"]
    print task2["rels"]
    print task3["rels"]

    print task1["nons"]
    print task2["nons"]
    print task3["nons"]

    return render_to_response('base/performance_experiment.html', {'participant': uname, 'condition': condition, 't1_rels': task1["rels"] , 't1_nons': task1["nons"], 't1_title': task1["title"], 't1_score': task1["score"], 't2_rels': task2["rels"] , 't2_nons': task2["nons"], 't2_title': task2["title"], 't2_score': task2["score"],'t3_rels': task3["rels"] , 't3_nons': task3["nons"], 't3_title': task3["title"], 't3_score': task3["score"]  }, context)
