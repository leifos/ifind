# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class RottenTomatoes(SearchEngine):
  """
  Rotten Tomatoes search engine.

  You must include your application's Rotten Tomatoes ID in your service manage config to use this service
  it should be under the identifier "rotten_tomatoes_api_key" 

  Parameters:

  * resultsPerPage (int): How many results per page
  """
    
  def __init__(self, service, resultsPerPage = 8, **args):
    super(RottenTomatoes, self).__init__(service, **args)
    self.resultsPerPage = resultsPerPage

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Rotten Tomatoes """
    return 1
    
  def search(self, query, offset):
    """
    Search function for Rotten Tomatoes Search.        
    
    Parameters:
    
    * query (puppy.model.Query)
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError    
    """
    
    def parse_rotten_tomatoes_json(site, pos, query, results):
      """      
      Rotten Tomatoes's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
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
      response.feed.setdefault('link', results['links']['self'])
      response.feed.setdefault('description', "Search results for '{0}' at {1}".format(query, site))
      response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
      
      try:
        response.feed.setdefault("opensearch_totalresults", int(results['total']))
        response.feed.setdefault("opensearch_itemsperpage", self.resultsPerPage)
        response.feed.setdefault("opensearch_startindex", pos)
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results['movies']:
        try:
          movie_dict = result
          movie_dict['link'] = result['links']['alternate']
          movie_dict['summary'] = result['synopsis']
          response.entries.append(movie_dict)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      
      return response

	# Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["rotten_tomatoes_api_key"]
    except KeyError:
      raise ApiKeyError("Rotten Tomatoes", "rotten_tomatoes_api_key")

    # Now that an API key has been supplied try to get results from the search engine itself
    try:    
      pos = self._origin() + offset
      url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey={0}&q={1}&page_limit={2}&page={3}".format(appId, urllib2.quote(query.search_terms), int(self.resultsPerPage), pos)
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_rotten_tomatoes_json('Rotten Tomatoes', pos, query.search_terms, results)

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Rotten Tomatoes", e, errorType = 'urllib2', url = url)

	# Check for a value error with resultsPerPage
    except ValueError, e:
      note = "Please ensure that 'resultsPerPage' is an integer."
      raise SearchEngineError("Rotten Tomatoes", e, note = note, resultsPerPageType = type(self.resultsPerPage))

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are both integers."
      if isinstance(offset, int) == False:
        raise SearchEngineError("Rotten Tomatoes", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Rotten Tomatoes", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("Rotten Tomatoes", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Rotten Tomatoes", e, url = url)