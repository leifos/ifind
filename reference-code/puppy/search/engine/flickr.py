# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class Flickr(SearchEngine):
  """
  Flickr search engine.

  You must include your application's Flickr ID in your service manage config to use this service
  it should be under the identifier "flickr_api_key" 


  Parameters:

  * sortBy (str):  how we sort results, default is relevance see Flickr API for more details

  * safeSearch (int): default is 3, i.e. strict, not recommended to change this

  * mediaType (str): all, photos, videos are the options

  * resultsPerPage (int): How many results per page

  * bbox (str): replace the names with the values of the corners of the bounding box 'swLongitude,swLatitude,neLongitude,neLatitude'
  """
    
  def __init__(self, service, sortBy = 'relevance', safeSearch = 3, mediaType = 'photos', resultsPerPage = 8, bbox = None, **args):
    super(Flickr, self).__init__(service, **args)
    self.sortBy = sortBy
    self.safeSearch = safeSearch
    self.mediaType = mediaType
    self.resultsPerPage = resultsPerPage
    self.bbox = bbox

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Flickr """
    return 1
    
  def search(self, query, offset):
    """Search function for Flickr Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)
    
    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_flickr_json(site, query, results):
      """Create a OpenSearch Response from Flickr results.
      
      Flickr's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
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
        response.feed.setdefault("opensearch_totalresults", int(results['total']))
        response.feed.setdefault("opensearch_itemsperpage", int(results['perpage']))
        response.feed.setdefault("opensearch_startindex", int(results['page']))
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      if 'photo' in results:
        for result in results['photo']:
          # Links need to be created from several fields - see the Flickr API for a detailed explanation
          
          try:
            resultLink = "http://www.flickr.com/photos/{0}/{1}".format(result['owner'], result['id'])
            resultThumbnail = "http://farm{0}.static.flickr.com/{1}/{2}_{3}_t.jpg".format(result['farm'], result['server'], result['id'], result['secret'])
            resultSummary = "Photo result for '{0}' from {1}".format(query, site)
            response.entries.append({'title': result['title'], 'link': resultLink, 'summary': resultSummary, 'thumbnail': resultThumbnail})
          except Exception, e:
            print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, results['link'])
            continue
            
      return response

	# Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["flickr_api_key"]
    except KeyError:
      raise ApiKeyError("Flickr", "flickr_api_key")

    # Now that an API key has been supplied try to get results from the search engine itself
    try:    
      pos = self._origin() + offset
      appId = self.service.config["flickr_api_key"]
      url = "http://api.flickr.com/services/rest/?method=flickr.photos.search&api_key={0}&text={1}&sort={2}&safe_search={3}&media={4}&per_page={5}&page={6}&format=json&nojsoncallback=1".format(appId, urllib2.quote(query.search_terms), self.sortBy, self.safeSearch, self.mediaType, self.resultsPerPage, pos)
      
      if (self.bbox):
        url += "&bbox={0}".format(self.bbox)   
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      results['photos'].setdefault(u'link', url)
      return parse_flickr_json('Flickr', query.search_terms, results['photos'])

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Flickr", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("Flickr", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Flickr", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("Flickr", e, note = note)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Flickr", e, url = url)