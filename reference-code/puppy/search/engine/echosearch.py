# -*- coding: utf8 -*-

from puppy.search import SearchEngine
from puppy.model import Query, Response

class EchoSearch(SearchEngine):
  """Testing search engine.
  
  TODO: move to tests folder or delete
  """
  
  def __init__(self, service):
    super(EchoSearch, self).__init__(service)
  
  
  def search(self, query, offset):
    """Echo search funcion.
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * results (puppy.model.Response)
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def create_echo_response(query, offset):
      """Create a Response from the query.
      
      The response repeats the terms of the query - only useful for debugging purposes.
      
      Parameters:
      
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * offset (int): result offset
      
      Returns:
      
      * results (puppy.model.Response)
      
      """
      
      response = Response()
      response.version = 'test'
      response.feed.setdefault('title', "EchoSearch")
      response.feed.setdefault('link', "www.puppyIR.eu")
      response.feed.setdefault('description', "Search engine for testing purposes")
      response.feed.setdefault('query', query.search_terms)
      
      query_list = query.search_terms.split()
      for term in query_list:
        response.entries.append({
          'title': term,
          'link': "http://www."+term+".com", 
          'summary': term
        })
      return response
    
    return create_echo_response(query, offset)
  

