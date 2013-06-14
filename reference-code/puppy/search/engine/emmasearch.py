# -*- coding: utf8 -*-

import urllib2

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class EmmaSearch(SearchEngine):
  """
  EmmaSearch search engine.

  Parameters:

  * age (str): values - 'v' for adults (shows all 'a' and 'k' results too), 'a' for teenagers, and 'k' for children

  * resultsPerPage (int): How many results per page - the default for the emma search service is 10
  """
  
  def __init__(self, service, age = 'v', resultsPerPage = 10, **args):
    super(EmmaSearch, self).__init__(service, **args)
    self.age = age
    self.resultsPerPage = resultsPerPage

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Emma search """
    return 1

  # Go through and extract the item's id from the link
  def addEmmaItemId(self, emmaResponse):
    for result in emmaResponse.entries:
      link = result['link']
      result['id'] = link[link.find("item=")+5:len(link)]
    return emmaResponse

  # Go through each result and assign based on the puppy_age parameter and numeric age classification to the results
  def addEmmaAge(self, emmaResponse):	 
    for result in emmaResponse.entries:
      if result.has_key('puppy_age'):
        if result['puppy_age'] == 'v':
          result['minAge'] = 20
          result['maxAge'] = 100
        elif result['puppy_age'] == 'a':
          result['minAge'] = 13
          result['maxAge'] = 19
        elif result['puppy_age'] == 'k':
          result['minAge'] = 0
          result['maxAge'] = 12
    return emmaResponse
    
  def search(self, query, offset):
    """
    Search function for retrieving results from the PuppyIR Pathfinder service which searches the information centre at the Emma Children's Hospital.
  
    Parameters:
  
    * query (puppy.model.Query)

    * offset (int): result offset for the search
  
    Returns:
  
    * results puppy.model.Response
  
    Raises:
  
    * urllib2.URLError
  
    """
    try:
      pos = self._origin() + offset
      format = 'rss'
      url = "http://pathfinder.cs.utwente.nl/cgi-bin/opensearch/ekz.cgi?query={0}&page={1}&format={2}&leeftijd={3}&size={4}".format(urllib2.quote(query.search_terms), pos, format, self.age, self.resultsPerPage)
    
      data = urllib2.urlopen(url)
      emmaResponse = Response.parse_feed(data.read())
      emmaResponse = self.addEmmaAge(emmaResponse)
      emmaResponse = self.addEmmaItemId(emmaResponse)
      return emmaResponse

	# urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("PuppyIR Pathfinder Search", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("PuppyIR Pathfinder Search", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("PuppyIR Pathfinder Search", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("PuppyIR Pathfinder Search", e, note = note)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("PuppyIR Pathfinder Search", e, url = url)