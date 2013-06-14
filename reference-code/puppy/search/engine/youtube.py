# -*- coding: utf8 -*-

import urllib2

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class YouTube(SearchEngine):
  """YouTube search engine."""
  
  def __init__(self, service, **args):
    super(YouTube, self).__init__(service, **args)

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Youtube """
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

    try:
      pos = self._origin() + offset    
      url = 'http://gdata.youtube.com/feeds/api/videos?vq={0}&racy=exclude&orderby=viewCount&start-index={1}'.format(urllib2.quote(query.search_terms), pos)
    
      data = urllib2.urlopen(url)
      return Response.parse_feed(data.read())

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("YouTube", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
          raise SearchEngineError("YouTube", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
          raise SearchEngineError("YouTube", e, note = note, resultsPerPageType = type(self.resultsPerPage))

	  raise SearchEngineError("YouTube", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("YouTube", e, url = url)