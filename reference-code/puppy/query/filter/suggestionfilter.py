import urllib2
import json

from puppy.query import QueryFilter
from puppy.model import Query

class SuggestionFilter(QueryFilter):
  """Creates a set of suggestions based upon the query search terms.
  
  As of July 2011, Sergio's web service no longer responds and is therefore not usable.

  Paramters:

  * order (int): filter precedence
  """
  
  def __init__(self, order=0):
    super(SuggestionFilter, self).__init__(order)
    self.description = "Creates a set of suggestions based upon the query search terms, and adds query['suggestions'] to query."
    
            
  def run(self, query):
    """
    Decorates a query with a set of suggestions.
    
    Parameters:
    
    * query (puppy.model.Query): original query
    
    Returns:
    
    * query (puppy.model.Query): query with suggestions
    
    Raises:
    
    * nothing really, just defaults the suggestions if Sergio's server is down
    """
    try:
      expandurl = 'http://130.89.11.231:8080/puppyWebForm/QueryDemo?query=' + query.search_terms
      expresponse = urllib2.urlopen(expandurl).read()
      suglist = json.loads(expresponse)
      sugdict = {}
      for s in suglist:
        if type(s) == list:
          popups = []
          if len(s) > 1:
            if type(s[1]) == list:
              popups = s[1]
          addfirst = []
          for p in popups:
            if type(p) == list:
              addfirst.append(p[0])
              popups.remove(p)
          popups += addfirst
          sugdict[s[0]] = popups
      query.suggestions = sugdict
      return query
    except Exception, e :
      # print 'Error in QuerySuggester: Query expansion failed: ', query.search_terms, 'using default expansion'
      query.suggestions = {u'school': [u'science', u'reading', u'writing', u'social studies', u'arithmetic'], u'technology': [], u'news': [u'magazines', u'current'], u'puzzles': [], u'games':[u'online', u'flash']}
      return query
  
