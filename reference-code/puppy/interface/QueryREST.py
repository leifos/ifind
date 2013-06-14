# -*- coding: utf8 -*-

import django.utils.http
import django.utils.encoding

from puppy.service import Service
from puppy.search import SearchEngine
from puppy.query.filter import TermExpansionFilter
from puppy.query.filter import SuggestionFilter
from puppy.model import Query

from django.conf.urls.defaults import *
from django_restapi.resource import Resource

from django.http import Http404, HttpResponse

# Urls for a resource that does not map 1:1
# to Django models.

class QueryREST(Resource):

    #we only need to response the read petition
    # for calling this function, call to http://127.0.0.1:8000/queryrest/?query=elmo
    def read(self, request):
        print "REST service: read"

        q = request.GET.get('query')
        profile=request.GET.get('profile')

        if( q == None):
            #none to search
            print "Blank search"
            xmldata = '<searchresponse><error>Blank search</error></searchresponse>'
            responseXML = HttpResponse(xmldata, mimetype='text/xml', content_type='text/xml;charset=UTF-8')
            return responseXML

        if( profile!= None):
            print "Profile", profile
            # at this moment, we only admit a default profile

        print q
        q = q.strip(' ')
        q = q.strip('%20')
        #q = django.utils.http.urlquote(q)
        print q

        # I see 2 alternatives for the future, with profiles
        #   1st to move this to several independent python files, for loading it
        #       dinamicaly (like filters)
        #   2nd XML files describing the filters and parameters. It is slower, but
        #       new filters can be added by a REST interface
        service = Service()
            # set up services

        service.add_query_filter(TermExpansionFilter("--terms=for+kids"))
        service.add_query_filter(TermExpansionFilter("--terms=colouring+book"))

        service.add_search_suggestion(SuggestionFilter())
        #service.add_search_engine(SearchEngine('Pathfinder'))
        service.add_search_engine(SearchEngine('Yahoo'))

        query = Query(q)


        response = service.search(query)

        xmldata = responseToXML(response)

        responseXML = HttpResponse(xmldata, mimetype='text/xml', content_type='text/xml;charset=UTF-8')
        return responseXML

def responseToXML(response):


#        xmldata = '<searchresponse>\n'
#
#        xmldata += '<title>'+response.title+'</title>/'
#        xmldata += '<description>'+response.description+'</description>/'
#        xmldata += '<total_results>'+response.total_results+'</total_results>/'
#        xmldata += '<start_index>'+response.start_index+'</start_index>/'
#        xmldata += '<items_per_page>'+response.items_per_page+'</items_per_page>/'
#        xmldata += '<query>'+response.query+'</query>/'
#        xmldata += '<items>'
#        for item in response.items:
#            xmldata += '<query>'+response.query+'</query>/'
#        xmldata += '</items>'
#        xmldata += '</searchresponse>\n'


    xmldata = response.write_xml()


    print xmldata
    return xmldata

