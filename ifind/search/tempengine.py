__author__ = 'leif'
__author__ = 'leifos'

import urllib, urllib2
from BeautifulSoup import BeautifulSoup
from ifind.search.searchengine import SearchEngine
from ifind.search.response import Response

class BingWebSearch(SearchEngine):

    def __init__(self, proxy_host=None, api_key=None, **kwargs):
        SearchEngine.__init__(self, proxy_host, api_key, **kwargs)

        # if api_key is None raise exception APIKeyException
        self.rootURL = "https://api.datamarket.azure.com/Bing/SearchWeb/"


        # Create the API URL


    def set_query_format(self, query, format="ATOM"):
        if format not in ["ATOM","JSON"]:
            query.format = "ATOM"
        else:
            query.format = format

    def issue_rest_request(self, query):
        """
        :param query: ifind.search.query.Query
        :return: url string for the rest request to the bing api
        """

        self.set_query_format(query,"ATOM")

        # REMEMBER: use apostrophes within the query search terms string, as this is what Bing expects
        quoted_query = urllib.quote("'"+ query.terms +"'" )
        searchURL = self.rootURL + "Web?$format=" + query.format + "&Query=" + quoted_query
        # Add the API key to the password manager
        print searchURL
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, searchURL, "", self.api_key)

         # Prepare an authentication handler and open the URL
        try:
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            xmlresponse = urllib2.urlopen(searchURL)
        except urllib2.URLError, e:
            raise e #SearchEngineError("Bing", e, errorType = 'urllib2', url = searchURL)

        return xmlresponse

    def parse_xml_response(self, query, xmlresponse):
        """
        map bing xml to ifind.search.response.Response object
        :param xmlresponse (xml string):
        :return: ifind.search.response.Response object
        """

        xmlSoup = BeautifulSoup(xmlresponse)

        response = Response()
        response.query_terms = query.terms

        resultCount = 0
        resultsRetrieved = 0
        for r in xmlSoup.findAll('entry'):
            xmlTitleData =  r.find('d:title').string
            xmlURLData =  r.find('d:url').string
            xmlDescriptionData = r.find('d:description').string
            response.add_result(xmlTitleData,xmlURLData,xmlDescriptionData)

        return response



    def search(self, query):
        """Search function for Microsoft Bing.

        Parameters:

        * query (ifind.search.query.Query)

        Returns:

            * ifind.search.response.Response

        Raises:

            * urllib2.URLError
            * API key error

        """

        xr = self.issue_rest_request(query)
        r = self.parse_xml_response(query,xr)
        return r
