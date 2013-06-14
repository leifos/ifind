# -*- coding: utf8 -*-
# coding=utf-8

import urllib, urllib2
from BeautifulSoup import BeautifulSoup
from puppy.model import Response
from puppy.search import SearchEngine
from puppy.search.exceptions import SearchEngineError, ApiKeyError

# Adapted from the PuppyIR framework available at
# http://sourceforge.net/projects/puppyir/
# for the search capabilities of PageFetch

# Changes: adapted to obtain as many results as we specify


class BingV3webonly(SearchEngine):

    def __init__(self, service, source = 'web', resultsPerPage = 10, **args):
        SearchEngine.__init__(self, service, **args)
        self.source = source
        self.resultsPerPage = resultsPerPage


    def search(self, query, offset):
        """Search function for Microsoft Bing.

       Parameters:

       * query (puppy.model.OpenSearch.Query)

       Returns:

       * puppy.model.OpenSearch.Response

       Raises:

       * urllib2.URLError

       """

        def parse_bing_xml_response(site, query, results, numResults=10, offset=0):

            xmlSoup = BeautifulSoup(results)

            response = Response()
            response.version = 'xml'
            response.feed.setdefault('title', "{0}: {1}".format(site, query))
            response.feed.setdefault('description', "Search results for {0} at {1}".format(query, site))
            response.feed.setdefault('link', '')
            response.namespaces.setdefault('opensearch', 'http://a9.com/-/spec/opensearch/1.1/')

            resultCount = 0
            resultsRetrieved = 0
            for r in xmlSoup.findAll('entry'):
                if (resultCount >= offset) and (resultCount < (numResults+offset)):
                    xmlTitleData =  r.find('d:title').string
                    xmlURLData =  r.find('d:url').string
                    xmlDescriptionData = r.find('d:description').string
                    response.entries.append({'title': xmlTitleData, 'link': xmlURLData, 'summary': xmlDescriptionData})
                    resultsRetrieved += 1
                resultCount += 1

            response.feed.setdefault('opensearch_totalresults', resultCount)
            response.feed.setdefault('opensearch_startindex', offset)
            response.feed.setdefault('opensearch_itemsperpage', resultsRetrieved)

            return response

        # Insert relevant details for Bing API here.
        username = ""
        try:
            appId = self.service.config["bing_api_key"]
            #print appId
        except KeyError:
            raise ApiKeyError("Bing V3", "bing_api_key")
        # Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
        queryBingFor = "'"+ query.search_terms +"'" # REMEMBER: use apostrophes within the string, this is what Bing expects
        quoted_query = urllib.quote(queryBingFor)

        # Create the API URL
        rootURL = "https://api.datamarket.azure.com/Bing/SearchWeb/"
        searchURL = rootURL + "Web?$format=ATOM&Query=" + quoted_query

        # Add the API key to the password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, searchURL, username, appId)

        # Prepare an authentication handler and open the URL
        try:
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            xmlresponse = urllib2.urlopen(searchURL)
        except urllib2.URLError, e:
            raise SearchEngineError("Bing V3", e, errorType = 'urllib2', url = searchURL)

        return parse_bing_xml_response('Bing V3', query.search_terms, xmlresponse, self.resultsPerPage, offset)