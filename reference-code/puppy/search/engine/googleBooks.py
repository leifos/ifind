# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class GoogleBooks(SearchEngine):
  """
  Google's Books search engine api.

  See Google's documentation for how to specify advanced queries e.g. Hobbit+inauthor:Tolkien

  Parameters:

  * resultsPerPage (int): How many results per page
  
  * langRestrict (str): restrict results to a certain language i.e. 'en' for English

  * filter (str): filter volumes by type/availabilty, valid values - 'partial', 'full', 'free-ebooks', 'paid-ebooks', 'ebooks'

  * orderBy (str): order either by 'relevance' or 'newest'

  * printType (str): 'all', 'books' or 'magazines' restrict the results to either all or one of the preceding types of media only

  """
    
  def __init__(self, service, resultsPerPage = 8, langRestrict = None, filter = None, orderBy = 'relevance', printType = None, **args):
    super(GoogleBooks, self).__init__(service, **args)
    self.resultsPerPage = resultsPerPage
    self.langRestrict  = langRestrict
    self.filter = filter
    self.orderBy = orderBy
    self.printType = printType
   
  def search(self, query, offset):
    """Search function for Google Books Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)
    
    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_google_books_json(site, url, pos, query, results):
      """Create a OpenSearch Response from Google Books results.
      
      Google Books's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
      * pos (int): what page number we are on
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
        response.feed.setdefault("opensearch_totalresults", int(results['totalItems']))
        response.feed.setdefault("opensearch_itemsperpage", self.resultsPerPage)
        response.feed.setdefault("opensearch_startindex", pos)
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results['items']:
        try:
          book_dict = result
          book_dict['title'] = result['volumeInfo']['title']

          if 'subtitle' in result['volumeInfo']:
            book_dict['title'] += " {0}".format(result['volumeInfo']['subtitle'])
          
          book_dict['link'] = result['selfLink']

          if 'description' in result:
            book_dict['summary'] = result['description']
          else:
            book_dict['summary'] = '' # If there's in no description it's up to the app developer to make use of the other data
          response.entries.append(book_dict)
          
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      
      return response
    try:    
      pos = self._origin() + offset
      url = "https://www.googleapis.com/books/v1/volumes?q={0}&maxResults={1}&startIndex={2}&orderBy={3}".format(urllib2.quote(query.search_terms), self.resultsPerPage, pos, self.orderBy)

      if self.langRestrict: # If we want to restrict results to only a certain language
        url += "&langRestrict={0}".format(self.langRestrict)

      if self.filter: # If we want to filter the results by volume/availablity i.e. only ebooks or books with a free preview
        url += "&filter={0}".format(self.filter)

      if self.printType: # If we want to have: all, only books or only magazines
        url += "&printType={0}".format(self.printType)

      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_google_books_json('Google Books', url, pos, query.search_terms, results)

	# urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Google Books", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("Google Books", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Google Books", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("Google Books", e, note = note)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Google Books", e, url = url)