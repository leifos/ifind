# -*- coding: utf8 -*-

from puppy.service import SearchService
from puppy.model import Response
import sys

class SearchServiceIterable(SearchService):
  """A SearchService that can be used as an iterator"""
  
  def __init__(self, service_manager, name, query=None):
    """Constructor for Service."""

    super(SearchServiceIterable,self).__init__(service_manager,name)


    # for iterator
    self.query = query
    self.resultsBuffer = Response()
    # This is an indication about the Response is not a real response, and we need to ask for a real response in Next
    self.resultsBuffer.feed['opensearch_totalresults'] = sys.maxint
    self.next_result = 0    

  def set_query(self,query):
    """
      Sets the query

      It is mandatory to set a query, here or in the constractor. 
    """
    self.query = query

  def __iter__(self):
    """
    Iterator member function
    
    Parameters:
    
    * None
    
    Returns:
    
    * An iterarator for the object, in this case, the object itself
    """
    return self

  def next(self):
    """
    Iterator member function
    
    Parameters:
    
    * None
    
    Returns:
    
    * The next item of the iterator, the next entry in the results
    """
    #print " total results  ", self.resultsBuffer.get_totalresults()
    #print " items per page ", self.resultsBuffer.get_itemsperpage()
    if self.query == None:
      print "None to search!!"
      #None to search!! The loop has finished
      raise StopIteration
    if len(self.resultsBuffer.entries) == 0:
      #print self.resultsBuffer.get_totalresults(), " == ", self.next_result
      if (int(self.resultsBuffer.get_totalresults()) <= self.next_result):
        raise StopIteration
      self.resultsBuffer = self.search(self.query, self.next_result)
      self.next_result += int(self.resultsBuffer.get_itemsperpage())

    if len(self.resultsBuffer.entries) == 0:
      raise StopIteration
    else:
      return self.resultsBuffer.entries.pop(0)
      

  def pull(self, numberItems):
    """
    Iterator member function. It gives a list of results.

    Note: Usually, "pull" returns an iterator. Here it returns a list (that, in turn, is iterable), The reason is
    that the list is easy to store in a variable. It is the only easy way to repear the results, because when
    the exclusion filter change el number of responses, going backwards  
    
    Parameters:
    
    * NumberItems: Number of demanded items
    
    Returns:
    
    * A list with the next numberItems items.
    """        
    listItems = []
    for i,item in enumerate(self):
      if i < numberItems:
        listItems.append(item)
      else:
        break
    return listItems
    
  
