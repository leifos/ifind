# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class Yahoo(SearchEngine):
  """
  Yahoo search engine.

  You must include your application's Yahoo ID in your service manage config to use this service. It should be under the identifier "yahoo_api_key"
  """
    
  def __init__(self, service, **args):
    super(Yahoo, self).__init__(service, **args)  
    
  def search(self, query, offset):
    """Search function for Yahoo! BOSS Search.
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_yahoo_json(site, query, results):
      """Create a OpenSearch Response from Yahoo! BOSS results.
      
      Yahoo!'s search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      
      Returns:
      
      * puppy.model.OpenSearch.Response
      
      """
      response = Response()
      response.version = 'json'
      response.feed.setdefault('title', "{0}: {1}".format(site, query))
      response.feed.setdefault('link', results['link'])
      response.feed.setdefault('description', "Search results for '{0}' at {1}".format(query, site))
      response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
      
      try:
        response.feed.setdefault("opensearch_totalresults", int(results['totalhits']))
        response.feed.setdefault("opensearch_itemsperpage", int(results['count']))
        response.feed.setdefault("opensearch_startindex", int(results['start']))
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results['resultset_web']:
        try:
          response.entries.append({'title': result['title'], 'link': result['url'], 'summary': result['abstract']})
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      
      return response

	# Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["yahoo_api_key"]
    except KeyError:
      raise ApiKeyError("Yahoo!", "yahoo_api_key")

    # Now that an API key has been supplied try to get results from the search engine itself
    try:    
      pos = self._origin() + offset
      url = "http://boss.yahooapis.com/ysearch/web/v1/{0}?appid={1}&format=json&style=raw&filter=-porn-hate&start={2}".format(urllib2.quote(query.search_terms), appId, str(pos))
    
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_yahoo_json('Yahoo!', query.search_terms, results['ysearchresponse'])

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Yahoo!", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset
    except TypeError, e:
      if isinstance(offset, int) == False:
        note = "Please ensure that 'offset' is an integer."
        raise SearchEngineError("Yahoo!", e, note = note, offsetType = type(offset))

      raise SearchEngineError("Yahoo!", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Yahoo!", e, url = url)