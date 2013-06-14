# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class Solr(SearchEngine):
  """Solr search engine."""
  
  def __init__(self, service, url, **args):
    super(Solr, self).__init__(service, **args)
    self.url = url  
  
  def search(self, query, offset):
    """Search function for solr-lucene.
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_yahoo_json(self, site, query, results):
      """Create a OpenSearch Response from Solr/Lucene results.
      
      We choose to ask for results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      
      Returns:
      
      * OpenSearch.Response
      
      """
      response = Response()
      response.version = 'json'
      response.feed.setdefault('title', "{0}: {1}".format(site, query))
      response.feed.setdefault('link', results['link'])
      response.feed.setdefault('description', "Search results for '{0}' at {1}".format(query, site))
      
      response.feed.setdefault('total_results', results['numFound'])
      response.feed.setdefault('start', results['start'])
      
      for result in results['docs']:
        response.entries.append({"title": result['title'][0], "link":result['attr_stream_name'][0], "summary":result['attr_content'][0]})
      
      return response

    try:    
      pos = self._origin() + offset
      url = "{0}/select?q=attr_content:{1}&wt=json&start={2}".format(self.url, urllib2.quote(query.search_terms), str(pos))
      response = urllib2.urlopen(url)
      results = json.loads(response)
      return parse_yahoo_json('Solr/Lucene', query.search_terms, results['response'])

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Solr/Lucene", e, errorType = 'urllib2', url = url)