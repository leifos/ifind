# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class Guardian(SearchEngine):
  """
  Guardian search engine api for searching for news stories.

  Warning: 'StandFirst' is the result field used for description; it is a form of abstract for the news story. It can however, contain html tags and so 
  when processing these results in an application this needs to be taken into account.

  Parameters:

  * orderBy (str): the options are - 'newest', 'oldest' and 'relevance'

  """
    
  def __init__(self, service, orderBy = 'newest', **args):
    super(Guardian, self).__init__(service, **args)
    self.orderBy = orderBy
    
  def search(self, query, offset):
    """Search function for Guardian News Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_guardian_json(site, url, query, results):
      """Create a OpenSearch Response from Guardian results.
      
      Guardians's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      
      Returns:
      
      * puppy.model.OpenSearch.Response
      
      """
      response = Response()
      response.version = 'json'
      response.feed.setdefault('title', "{0}: {1}".format(site, query))
      response.feed.setdefault('link', url)
      response.feed.setdefault('description', "Search results for '{0}' at {1}".format(query, site))
      response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
      try:
        response.feed.setdefault("opensearch_totalresults", int(results['total']))
        response.feed.setdefault("opensearch_itemsperpage", int(results['pageSize']))
        response.feed.setdefault("opensearch_startindex", int(results['startIndex']))
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results['results']:
        try:
          response.entries.append({'title': result['webTitle'], 'link': result['webUrl'], 'summary': result['fields']['standfirst']})
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      
      return response
      
    try:
      url = "http://content.guardianapis.com/search?q={0}&format=json&show-fields=standfirst&order-by={1}".format(urllib2.quote(query.search_terms), self.orderBy)
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_guardian_json('Guardian', url, query.search_terms, results['response'])

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Guardian", e, errorType = 'urllib2', url = url)
      
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Guardian", e, url = url)