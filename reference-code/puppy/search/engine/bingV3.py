# -*- coding: utf8 -*-
# coding=utf-8

import urllib, urllib2
from BeautifulSoup import BeautifulSoup
from puppy.model import Response
from puppy.search import SearchEngine
from puppy.search.exceptions import SearchEngineError, ApiKeyError


class BingV3(SearchEngine):

    def __init__(self, service, source = 'Web', resultsPerPage = 10, **args):
        """
        Args:
            source - should be 'Web', 'Image', 'News', 'RelatedSearch', 'SpellingSuggestions'
        """
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

        def parse_bing_xml_response(site, query, results, offset=0):



            def extractElementString(node, element):
                res =node.find(element)
                if res:
                    return res.string
                else:
                    return ''

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

                # These element are in Web
                xmlTitleData = extractElementString(r, 'd:title')
                xmlURLData = extractElementString(r,'d:url')
                xmlDescriptionData = extractElementString(r,'d:description')
                # These elements are in News
                xmlSource = extractElementString(r, 'd:source')
                xmlDate = extractElementString(r, 'd:date')

                result_dict = {'title': xmlTitleData, 'link': xmlURLData, 'summary': xmlDescriptionData, 'source': xmlSource, 'date': xmlDate }

                # These elements are in Images
                xmlLink = extractElementString(r, 'd:mediaurl')
                if xmlLink: result_dict['link'] = xmlLink

                xmlSourceUrl = extractElementString(r, 'd:sourceurl')
                if xmlSourceUrl: result_dict['sourceLink'] = xmlSourceUrl

                xmlDisplayLink = extractElementString(r,'d:displayurl')
                if xmlDisplayLink: result_dict['displayLink'] = xmlDisplayLink

                xmlWidth = extractElementString(r,'d:width')
                if xmlWidth: result_dict['width'] = xmlWidth

                xmlHeight = extractElementString(r,'d:height')
                if xmlHeight: result_dict['height'] = xmlHeight

                thumbnail = r.find('d:thumbnail')

                if thumbnail:
                    xmlThumbnail = extractElementString(thumbnail,'d:mediaurl')
                    if xmlThumbnail: result_dict['thumbnail'] = xmlThumbnail

                    xmlThumbnailWidth = extractElementString(thumbnail,'d:width')
                    if xmlThumbnailWidth: result_dict['thumbnailWidth'] = xmlThumbnailWidth

                    xmlThumbnailHeight = extractElementString(thumbnail,'d:height')
                    if xmlThumbnailHeight: result_dict['thumbnailHeight'] = xmlThumbnailHeight



                response.entries.append(result_dict)
                resultsRetrieved += 1
                resultCount += 1

            response.feed.setdefault('opensearch_totalresults', resultCount+offset)
            response.feed.setdefault('opensearch_startindex', offset)
            response.feed.setdefault('opensearch_itemsperpage', resultsRetrieved)

            return response

        # Insert relevant details for Bing API here.
        username = ""
        try:
            appId = self.service.config["bing_api_key"]
        except KeyError:
            raise ApiKeyError("Bing V3", "bing_api_key")
            # Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
        queryBingFor = "'"+ query.search_terms +"'" # REMEMBER: use apostrophes within the string, this is what Bing expects
        quoted_query = urllib.quote(queryBingFor)

        # Create the API URL
        rootURL = "https://api.datamarket.azure.com/Bing/Search/"
        searchURL = "%s%s?$format=ATOM&$top=%d&$skip=%d&Query=%s" % (rootURL, self.source, self.resultsPerPage, offset, quoted_query)
        #searchURL = rootURL + self.source + "?$format=ATOM&Query=" + quoted_query
        print searchURL

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

        return parse_bing_xml_response('Bing V3', query.search_terms, xmlresponse, offset)