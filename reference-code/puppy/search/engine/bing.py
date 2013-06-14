# -*- coding: utf8 -*-

import urllib2

from puppy.search.engine.site import sitesearch
from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class Bing(SearchEngine, sitesearch):
  """
  Bing search engine wrapper.

  Note: you can only use location based searching with sourcetypes 'web' and 'phonebook'; however, with web, it doesn't appear to have any effect.

  Parameters:

  * sites: if you wish to search a specific website(s) for results

  * source (str): web, image, news are the options

  * adult (str): strict, i.e. safesearch not recommended to change from the default

  * market (str): i.e. which area's results are prioritised more - en-gb is the UK

  * resultsPerPage (int): How many results per page

  * lat (double): the latitude of the place you want to search in

  * lon (double): the longitude of the place you want to search in

  * radius (int): the radius to retrieve results from around lat and lon; 0-250miles is the limit
  """
  
  def __init__(self, service, source = 'web', adult = 'Strict', market = 'en-GB', resultsPerPage = 10, lat = None, lon = None, radius = 5, sites=None, **args):
    SearchEngine.__init__(self, service, **args)
    sitesearch.__init__(self, sites)
    self.sites = sites
    self.source = source
    self.adult = adult
    self.market = market
    self.resultsPerPage = resultsPerPage
    self.lat = lat
    self.lon = lon
    self.radius = radius
  
   
  def search(self, query, offset):
    """
    Search function for Microsoft Bing.
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * results (puppy.model.Response)
    
    Raises:
    
    * urllib2.URLError
    """

    def addDefaultThumbnails(bingResponse):
      """This goes through the results and adds a easy access default thumbnail."""
      for result in bingResponse.entries:
        result['thumbnail'] = result['media_thumbnail'][0]['url']
        result['thumbnailWidth'] = result['media_thumbnail'][0]['width']
        result['thumbnailHeight'] = result['media_thumbnail'][0]['height']
      return bingResponse

    try:
      formattedQuery = urllib2.quote(self._modify_query(query.search_terms))
      pos = self._origin()

      if (offset > 0):
        pos = pos + (offset * self.resultsPerPage)   

      url = 'http://api.search.live.net/rss.aspx?&query={0}&source={1}&{1}.count={2}&{1}.offset={3}&Adult={4}&Market={5}'.format(formattedQuery, self.source, self.resultsPerPage, pos, self.adult, self.market)
      
      # If the source type is web or phonebook we can add lon/lat/radius for local search
      if(self.source == 'web') or (self.source == 'phonebook'):
        if (self.lat) and (self.lon) and (self.radius):
          url += "&Latitude={0}&Longitude={1}&Radius={2}".format(self.lat, self.lon, self.radius)
      
      data = urllib2.urlopen(url)
      bingResponse = Response.parse_feed(data.read())

      if self.source == 'image':
        bingResponse = addDefaultThumbnails(bingResponse)          
          
      return bingResponse

	# urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Bing", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("Bing", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Bing", e, note = note, resultsPerPageType = type(self.resultsPerPage))
	
      raise SearchEngineError("Bing", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Bing", e, url = url)