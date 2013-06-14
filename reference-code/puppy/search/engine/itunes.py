# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response

from puppy.search.exceptions import SearchEngineError

class ITunes(SearchEngine):
  """
  iTunes search engine wrapper - allowing for Track, Album and Artist search results to be retrieved

  If you change either lang or country change the other variable to match i.e. change lang to 'en_gb' you should also change
  country to 'gb' to match or vice-versa.

  Parameters:

  * country (str): Which iTunes store to search i.e. 'gb' for the UK and 'us' for the USA etc

  * lang (str): the language the results should be returned in

  * media(str): the media type you want to search for (see iTunes documentation for others e.g. 'movie' etc)

  * resultsPerPage (int): How many results per page

  * explicit (boolean): Do we want to return results marked as including explicit content (not recommended to change this)

  """
    
  def __init__(self, service, country = 'gb', lang = 'en_gb', media = None, resultsPerPage = 8, explicit = False, **args):
    super(ITunes, self).__init__(service, **args)
    self.country = country
    self.resultsPerPage = resultsPerPage
    self.explicit = explicit
    self.lang = lang
    self.media = media # If not supplied it defaults to 'all'

  def search(self, query, offset):
    """Search function for ITunes Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_itunes_json(site, url, query, results):
      """Create a OpenSearch Response from iTunes results.
      
      iTunes's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
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
        response.feed.setdefault("opensearch_totalresults", int(results['resultCount']))
        response.feed.setdefault("opensearch_itemsperpage", self.resultsPerPage)
        response.feed.setdefault("opensearch_startindex", 0)
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results['results']:
        try:
          result_dict = result
          result_dict['title'] = ''
          result_dict['link'] = ''

          # For ease of access if we have a thumbnail store it under that name as well
          if 'artworkUrl60' in result:
            result_dict['thumbnail'] = result['artworkUrl60']

          # If we have a trackname use it - this is iTunes's default for title
          if 'trackName' in result:
            result_dict['title'] = result['trackName']

            # Use censored track name instead if explicit content should be avoided
            if (self.explicit == False) and ('trackCensoredName' in result):
              result_dict['title'] = result['trackCensoredName']
            
            result_dict['summary'] = "{0} by {1}".format(result_dict['title'], result['artistName'])

          # Otherwise see if there's a collection name - if we have a collection of videos or songs it will use this not the above
          elif 'collectionName' in result:
            result_dict['title'] = result['collectionName']

            # Use censored collection name instead if explicit content should be avoided
            if (self.explicit == False) and ('collectionCensoredName' in result):
              result_dict['title'] = result['collectionCensoredName']

            result_dict['summary'] = "An item by {0} from the collection {1}".format(result['artistName'], result_dict['title'])

          # If we have a description then use this instead of the above for the summary
          if 'longDescription' in result:
            result_dict['summary'] = result['longDescription']
          elif 'shortDescription' in result:
            result_dict['summary'] = result['shortDescription']

          # Track is the default - same as above this is the iTunes default link for an item
          if 'trackViewUrl' in result:							
            result_dict['link'] = result['trackViewUrl']
            # Next check if there's a collection - if its a collection it will use this
          elif 'collectionViewUrl' in result:
            result_dict['link'] = result['collectionViewUrl']
          # Finally artist - this is the final fallback for a link to this item, a link to the artist page
          elif 'artistViewUrl' in result:
            result_dict['link'] = result['artistViewUrl']
            
          response.entries.append(result_dict)
          
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
  
      return response

    try:
      url = "http://itunes.apple.com/search?country={0}&term={1}&limit={2}&lang={3}".format(self.country, urllib2.quote(query.search_terms), self.resultsPerPage, self.lang)

      if self.explicit == False:
        url += "&explicit=No"

      if self.media:
        url += "&media={0}".format(self.media)

      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_itunes_json('iTunes', url, query.search_terms, results)

	# urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("iTunes", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      if isinstance(self.resultsPerPage, int) == False:
        note = "Please ensure that 'resultsPerPage' is an integer."
        raise SearchEngineError("iTunes", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("iTunes", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("iTunes", e, url = url) 