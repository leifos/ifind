# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class LastFm(SearchEngine):
  """
  LastFM search engine wrapper - allowing for Track, Album and Artist search results to be retrieved

  You must include your application's LastFM ID in your service manage config to use this service. It should be under the identifier "last_fm_api_key"

  Parameters:

  * source (str): What to search for, valid types: 'track', 'album' and 'artist'

  * resultsPerPage (int): How many results per page

  -- 'Track' Only Parameters --
  * artist (str): the artist for the tracks you are searching for
  """
    
  def __init__(self, service, source = 'track', resultsPerPage = 8, artist = None, **args):
    super(LastFm, self).__init__(service, **args)
    self.source = source
    self.resultsPerPage = resultsPerPage
    self.artist = artist

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for LastFM """
    return 1

  def search(self, query, offset):
    """
    Search function for LastFM Search.        
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_last_fm_json(site, url, query, results, pos):
      """      
      LastFM's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
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
        response.feed.setdefault("opensearch_totalresults", results['opensearch_totalresults'])
        response.feed.setdefault("opensearch_itemsperpage", results['opensearch_itemsperpage'])
        response.feed.setdefault("opensearch_startindex", pos)
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)

      if (self.source == 'track') and ('track' in results['trackmatches']):
        response.entries = parseLastFmResultsJson(results, 'trackmatches', 'track', url)
      elif (self.source == 'album') and ('album' in results['albummatches']):
        response.entries = parseLastFmResultsJson(results, 'albummatches', 'album', url)
      elif (self.source == 'artist') and ('artist' in results['artistmatches']):
        response.entries = parseLastFmResultsJson(results, 'artistmatches', 'artist', url)

      return response

    def parseLastFmResultsJson(results, matchesName, typeName, url):
      """Parses LastFm results and returns them ready to be added to response's entries."""
      parsedResults = []
    
      # If we have >1 results the format is a list, if 1 it's a dictionary so parse accordingly
      if isinstance(results[matchesName][typeName], list):
        for result in results[matchesName][typeName]:
          try:
            tempResult = processLastFmResult(result, typeName)
            parsedResults.append(tempResult)
          except Exception, e:
            print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
            continue
      else:
        try:
          tempResult = processLastFmResult(results[matchesName][typeName], typeName)
          parsedResults.append(tempResult)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)

      return parsedResults

    def processLastFmResult(result, typeName):
      """Processes an individual lastFM result and returns it as a dictionary."""
      result_dict = result
      result_dict["title"] = result['name']
      result_dict["link"] = result['url']

      if ('image' in result) and (len(result['image']) > 0): # If there are images add a shortcut to get a good thumbnail
        result_dict['thumbnail'] = result['image'][0]['#text']

      result_dict['summary'] = "{0}".format(result_dict['title'])

      if (typeName == 'track') or (typeName == 'album'):
        result_dict['summary'] += " by {0}".format(result_dict['artist'])

      if 'listeners' in result_dict:
        result_dict['summary'] += ", with {0} listeners".format(result_dict['listeners'])

      return result_dict

    # Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["last_fm_api_key"]
    except KeyError:
      raise ApiKeyError("LastFM", "last_fm_api_key")

    # Now that an API key has been supplied try to get results from the search engine itself
    try:
      pos = self._origin() + offset
      url = "http://ws.audioscrobbler.com/2.0/?method={0}.search&{0}={1}&api_key={2}&limit={3}&page={4}&format=json".format(self.source, urllib2.quote(query.search_terms), appId, self.resultsPerPage, pos)

      if self.artist and self.source == 'track':
        url += "&artist={0}".format(self.artist)

      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_last_fm_json('LastFM', url, query.search_terms, results['results'], pos)

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("LastFM", e, errorType = 'urllib2', url = url)

	# Check for a value error with resultsPerPage
    except ValueError, e:
      note = "Please ensure that 'resultsPerPage' is an integer"
      raise SearchEngineError("LastFM", e, note = note, resultsPerPageType = type(self.resultsPerPage))

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are both integers."
      if isinstance(offset, int) == False:
        raise SearchEngineError("LastFM", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("LastFM", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("LastFM", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("LastFM", e, url = url)