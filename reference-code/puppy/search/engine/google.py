# -*- coding: utf8 -*-

import urllib2
import socket
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response

class Google(SearchEngine):
  """Google search engine.
  
  Google have regrettfully retired this search api
  
  Code is left here for reference purposes
  """
  
  def __init__(self, service, **args):
    super(Google, self).__init__(service, **args)
  
  
  def search(self, query, offset):
    """Search function for Google AJAX Search.
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * results (puppy.model.Response)
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_google_json(site, url, query, num_results, results):
      """Create a OpenSearch Response from Google AJAX Search results.
      
      Google's search API returns results in JSON format. This function loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): search url used
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * num_results (int): number of desired results
      * results (dict): results from service
      
      Returns:
      
      * results (puppy.model.Response)
      
      """
      response = Response()
      response.version = 'json'
      response.feed.setdefault('title', "{0}: {1}".format(site, query))
      response.feed.setdefault('link',results['cursor']['moreResultsUrl'])
      response.feed.setdefault('description',"Search results for '{0}' at {1}".format(query, site))
      try:
        response.feed.setdefault('opensearch_totalresults',results['cursor']['estimatedResultCount'])
        response.feed.setdefault('opensearch_startindex', results['cursor']['currentPageIndex'])
      except KeyError:
        response.feed.setdefault('opensearch_totalresults',0)
        response.feed.setdefault('opensearch_startindex', 0)
      
      for result in results['results']:
        response.entries.append( { 'title':result['title'],'link':result['url'], 'summary':result['content'] })
      
      response.feed.setdefault('opensearch_itemsperpage',len(response.entries))   
      return response
    
    ip_addr = socket.gethostbyname(socket.gethostname())
    num_results = 8
    pos = self._origin() + offset
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q={0}&key={1}&userip={2}&rsz={3}&start={4}".format(urllib2.quote(query.search_terms), self.service.config["google_api_key"], ip_addr, num_results, pos)
    
    try:
      request = urllib2.Request(url, None, {'Referer': "http://www.dcs.gla.ac.uk"})
      response = urllib2.urlopen(request)
      print str(response)
      results = json.loads(str(response))
      return parse_google_json('Google', url, query.search_terms, num_results, results['responseData'])
    except urllib2.URLError, e:
      print "Error in SearchService: Google AJAX Search failed"
