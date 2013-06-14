# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response

from puppy.model import Query, Response
from puppy.query.exceptions import QueryRejectionError

# Service
from mase.service import service

# From Settings
from settings import ONDOLLEMAN, DOLLEMANPATH

import os

if ONDOLLEMAN:
	queryLogDir = DOLLEMANPATH
else:
    queryLogDir = os.getcwd()

def test(request):
    """show base index view"""
    context = RequestContext(request)
    return render_to_response('mase/test.html', context)

def index(request):
    """show base index view"""
    context = RequestContext(request)
    query_flag = False
    if request.method =='POST':
        user_query = request.POST['query']
        query_flag = True
    elif request.method == 'GET':
        getdict = request.GET
        if 'query' in getdict:
    	    user_query = getdict['query']
    	    query_flag = True

    result_dict = {}
    if 'searchEngineName' in request.POST:
        result_dict['searchEngineTitle'] = request.POST['searchEngineName']
    if query_flag:
        query = Query(user_query)
        result_dict['query'] = user_query
        result_dict['pastQueries'] = queryLog()            
        return results(request, query, result_dict)
    else:
        return render_to_response('mase/index.html', context)

def queryLog():
    try:
        queries = {}
        f = open(queryLogDir + '/mase/query_logs/web_search_query_log', 'r')
        
        for line in f:
            tempQuery = line.split(', ')
            if len(tempQuery) == 2:
                query = tempQuery[1]
                query = query[0:len(query)-1]
                if query not in queries: # Only add unique queries - duplicate queries don't add extra value
                    queries[query] = query
        f.close()
        #queries = queries[:len(queries)-2] + '.'
        return list(queries)
    except IOError:
        print("Failed")
        pass

# Method to add a short version of the URL for descriptive purposes to show the source website
def addShortUrls(results):
    for result in results:
        shortUrl = result['link']
        if shortUrl.find('www.') >= 0:	# If there's www. remove it
            shortUrl = shortUrl[shortUrl.find('www.') + 4:]
        if shortUrl.find('http://') >= 0:	#If there's http:// remove it
            shortUrl = shortUrl[shortUrl.find('http://') + 7:]
        if shortUrl.find('/') >= 0:
            shortUrl = shortUrl[0:shortUrl.find('/')] # Get rid of the detail for example bbc.co.uk instead of bbc.co.uk/news/
        result['shortUrl'] = ' [' + shortUrl +']'
    return list(results)

def results(request, query, result_dict):
    context = RequestContext(request)
              
    #check if web_search exists, if so, include web results        
    if 'web_search' in service.search_services:
        try:
            result_dict['web_search'] = True
            web_results = service.search_services['web_search'].search( query ).entries
            result_dict['web_results'] = addShortUrls(web_results)
        except QueryRejectionError:
            result_dict['webQueryRejected'] = True

    if 'news_search' in service.search_services:
        try:            
            result_dict['news_search'] = True
            news_results = service.search_services['news_search'].search( query ).entries
            result_dict['news_results'] = addShortUrls(news_results)
        except QueryRejectionError:
            result_dict['newsQueryRejected'] = True

    if 'wiki_search' in service.search_services:
        try:            
            result_dict['wiki_search'] = True
            wiki_results = service.search_services['wiki_search'].search( query ).entries
            result_dict['wiki_results'] = list(wiki_results)
        except QueryRejectionError:
            result_dict['wikiQueryRejected'] = True

    if 'image_search' in service.search_services:
        try:            
            result_dict['image_search'] = True
            image_results = service.search_services['image_search'].search( query ).entries
            result_dict['image_results'] = list(image_results)
        except QueryRejectionError:
            result_dict['imageQueryRejected'] = True

    if 'video_search' in service.search_services:
        try:            
            result_dict['video_search'] = True
            video_results = service.search_services['video_search'].search( query ).entries
            result_dict['video_results'] = list(video_results)
        except QueryRejectionError:
            result_dict['videoQueryRejected'] = True

        # check if twitter_search exists, if so, include twitter_results
    if 'twitter_search' in service.search_services:
        try:            
            result_dict['twitter_search'] = True
            twitter_results = service.search_services['twitter_search'].search( query ).entries
            result_dict['twitter_results'] = list(twitter_results)
        except QueryRejectionError:
            result_dict['twitterQueryRejected'] = True
                   
        # check if query_suggest_search exists, if so include query_results
    if 'query_suggest_search' in service.search_services:
        result_dict['query_suggest_search'] = True
        query_suggest_results = service.search_services['query_suggest_search'].search( query ).entries
        result_dict['query_suggest_results'] = list(query_suggest_results)


		 # check if query_suggest_search exists, if so include query_results
    if 'spelling_suggestion_service' in service.search_services:
        result_dict['spelling_suggestion'] = True
        spelling_suggestion_results = service.search_services['spelling_suggestion_service'].search( query ).entries
        result_dict['spelling_suggestion_results'] = list(spelling_suggestion_results)

    return render_to_response('mase/index.html', result_dict, context)