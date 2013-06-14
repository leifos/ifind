# -*- coding: utf8 -*-

import urllib2

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class YouTubeV2(SearchEngine):
  """
  YouTube search engine API version 2.

  The orderBy parameter allows results to be filtered by their language relevence - see below for more.
  
  N.B. in the text below replace <languageCode> with a code i.e. English: 'en', Dutch: 'nl' depending upon your applications needs.

  Parameters:

  * resultsPerPage (int): results per page
  
  * safeSearch (str) : default is strict it's not recommended to change this

  * orderBy: (str)  rating, viewCount, relevance, relevance_lang_<languageCode>

  * format (int): this defines if videos must conform to a standard for example 5 means only videos that can be embedded
      
  * location (str): defines the location the videos should be from, in the format 'lat,lon'
      
  * locationRadius (str): format is '<radius><unit>' the radius around the location, within which results should be return from
                          the valid units are: m, km, ft and mi
      
  * onlyLocation (boolean): only return results with a location (i.e. a geotag) 
  """
  
  def __init__(self, service, resultsPerPage = 8, safeSearch = 'strict', orderBy = 'relevance', format = None, location = None, locationRadius = None, onlyLocation = False, **args):
    super(YouTubeV2, self).__init__(service, **args)
    self.resultsPerPage = resultsPerPage
    self.safeSearch = safeSearch
    self.orderBy = orderBy
    self.format = format
    self.location = location
    self.locationRadius = locationRadius
    self.onlyLocation = onlyLocation    

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Youtube V2 """
    return 1

  def search(self, query, offset):
    """
    Search function for YouTube.
    
    Parameters:
    
    * query (puppy.model.OpenSearch.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.OpenSearch.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    def addExtraFields(youtubeResponse):
      """This goes through the results and adds: the summary field, the embed url and adds a thumbnail shortcut."""
      for result in youtubeResponse.entries:
        author = result['author']
        fullDescription = result['media_group'] # This is author+description+'youtube'
        result['summary'] = fullDescription[len(author):len(fullDescription)-7] #Remove author from start and 'youtube' from end - Perhaps find more elegant method
        result['embedUrl'] = 'http://www.youtube.com/embed/' + result['id'].split(':video:')[1]

        if len(result['media_thumbnail']) >= 2: # If we have 2 or more thumbnails use the second (hq thumbnail)
          result['thumbnail'] = result['media_thumbnail'][1]['url']
        elif len(result['media_thumbnail']) == 1: # Otherwise use the first (it's pretty low res compared to above)
          result['thumbnail'] = result['media_thumbnail'][0]['url']
        else:
          result['thumbnail'] = '' # If that fails just leave it blank

      return youtubeResponse
      
    try:
      pos = self._origin() + (offset * self.resultsPerPage)
      url = 'http://gdata.youtube.com/feeds/api/videos?q={0}&max-results={1}&safeSearch={2}&start-index={3}&orderby={4}&v=2'.format(urllib2.quote(query.search_terms), self.resultsPerPage, self.safeSearch, pos, self.orderBy)
    
      if self.format:
        url += "&format={0}".format(self.format)
            
      if self.location and self.locationRadius:
        url+= "&location-radius={0}&location={1}".format(self.locationRadius, self.location)
        if self.onlyLocation == True:
          url += '!' # This forces YouTube to only return results with a location 

      data = urllib2.urlopen(url)
      youtubeResponse = Response.parse_feed(data.read())
      youtubeResponse = addExtraFields(youtubeResponse) # Does some processing to get embed url, summary and thumbnail shortcut
      return youtubeResponse

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("YouTube V2", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("YouTube V2", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("YouTube V2", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("YouTube V2", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("YouTube V2", e, url = url)