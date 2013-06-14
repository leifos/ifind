# -*- coding: utf8 -*-

import urllib2

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class Twitter(SearchEngine):
  """
  Twitter search engine.
  
  Geocode format is: latitude,longitude,radius - for example: '37.781157,-122.398720,1mi'

  Parameters:

  * language (str): en = English, de = German etc

  * type (str): what sort of results to get can be - mixed, recent, popular

  * geocode (str): to get queries around a specific location

  * includeEntities (boolean): if this is true then a lot of meta-data is included (mentions, associated images, associated urls)

  * resultsPerPage (int): results per page

  
  """
  
  def __init__(self, service, language = 'en', type = 'mixed', geocode = None, resultsPerPage = 9, includeEntities = False, **args):
    super(Twitter, self).__init__(service, **args)
    self.language = language
    self.type = type
    self.geocode = geocode
    self.resultsPerPage = resultsPerPage
    self.includeEntities = includeEntities

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Twitter """
    return 1  
  
  def search(self, query, offset):
    """
    Search function for Twitter.
    
    Parameters:
    
    * query (puppy.model.OpenSearch.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError    
    """    
    try:	
      pos = self._origin() + offset   
      url = 'http://search.twitter.com/search.atom?q={0}&lang={1}&page={2}&result_type={3}&rpp={4}&include_entities={5}'.format(urllib2.quote(query.search_terms), self.language, pos, self.type, self.resultsPerPage, self.includeEntities)
	 
      if self.geocode:
        url += '&geocode:{0}'.format(self.geocode)

      data = urllib2.urlopen(url)
      return Response.parse_feed(data.read())

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Twitter", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("Twitter", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Twitter", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("Twitter", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Twitter", e, url = url)