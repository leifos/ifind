.. _extending_the_search_engine:

Adding new Search Engine Wrappers 
=======================================

This section details adding new search engine wrappers.

Creating new Search Engine Wrappers
***********************************

Every search engine wrapper must extend the base class SearchEngine. This base class defines the standard attributes common to all search engine wrappers and also provides the facility to use a search engine wrapper using a proxy server, if this is required. The key aspect, for new search engine wrappers, is that the search method must be overwritten in them (to handle the retrieving of and processing of results from the external web service the wrapper is for).


The SearchEngine base class is included below for reference purposes:

::

  # -*- coding: utf8 -*-

  import urllib2

  class SearchEngine(object):
    """Abstract search engine interface."""

    def __init__(self, service, **args):
      """
      Constructor for SearchEngine.

      Parameters:

      * service (puppy.service.SearchService): A reference to the parent search service
      * options (dict) a dictionary of engine specific options
      """
      self.name = self.__class__.__name__
      self.service = service
      self.configure_opener()

      # Prints invalid parameters received for the Search Engine
      for parameter in args:
          print "'{0}' received invalid parameter called: '{1}'".format(self.name, parameter)

    def _origin(self):
      """ This defines the default origin for results from a search engine """
      return 0


    def configure_opener(self):
      """Configure urllib2 opener with network proxy"""

      if "proxyhost" in self.service.config:
        proxy_support = urllib2.ProxyHandler({'http': self.service.config["proxyhost"]})
        opener = urllib2.build_opener(proxy_support)
      else:
        opener = urllib2.build_opener()
      urllib2.install_opener(opener)


    def search(self, query, pos=1):
      """
      Perform a search.

      Parameters:

      * query (puppy.model.Query): query object
      * pos (int): result offset

      Returns:

      * results (puppy.model.Response): results of the search

      """
      pass

Example Search Engine Wrapper
---------------------------------

For example, a **Picassa** (an online image sharing website) wrapper for retrieving image results is included below.

The search method must be passed a Query object (:ref:`puppy_query`) and return a Response object (:ref:`puppy_response`). In this example, the processing of the results is handled by the Response class itself - as the data format from Picassa is an Atom Feed, which can be parsed automatically by the framework.

::

  import urllib2

  from puppy.search import SearchEngine
  from puppy.model import Query, Response

  class Picassa(SearchEngine):
    """
    Picassa search engine.

    Parameters:

    * resultsPerPage (int): select how many results per page
    """
  
    def __init__(self, service, resultsPerPage=8, **args):
      super(Picassa, self).__init__(service, **args)
      self.resultsPerPage = resultsPerPage

    def _origin(self):
      """ This overrides SearchEngine's default origin as Picassa is 1-indexed """
      return 1
  
    def search(self, query, offset):
      """
      Search function for Picassa.
    
      Parameters:
    
      * query (puppy.model.OpenSearch.Query)
    
      Returns:
    
      * puppy.model.OpenSearch.Response
    
      Raises:
    
      * urllib2.URLError
    
      """

      pos = self._origin() + offset 
      userQuery = urllib2.quote(query.search_terms)
      url = "https://picasaweb.google.com/data/feed/api/all?q={0}&kind=photo".format(userQuery)

      # Add in the resultsPerPage parameter
      url += "&max-results={0}".format(self.resultsPerPage)

      # Add in pagination
      url += "&start-index={0}".format(pos)

      try:
        data = urllib2.urlopen(url)
        return Response.parse_feed(data.read())
      except urllib2.URLError, e:
        print "Error in Search Service: Picassa search failed"

Note, in the above example, what needs to be done to conform to the SearchEngine standard and how to construct a URL to get results from the external service.

Origin of the results
**********************************

Results from a search engine are generally either 0 or 1 indexed, depending upon the service in question. To account for this, as shown in the code of SearchEngine, there is an origin defined and each service uses the following code to work out the position for any offset/pagination parameters in the request to an external service (in the Picassa example the url variable is this request):

::

   pos = self._origin() + offset

The default is '0' and so, if a search engine is 1-indexed, for example, the search engine wrapper must override the origin in SearchEngine with its own version (the code for pos is unchanged):

::

  def _origin(self):
    """ This SearchEngine is 1-indexed so override the default"""
    return 1

Json and other formats
**********************************

The standard method, as detailed above, is for wrappers to parse RSS/Atom feeds to retrieve the results. However, not all API's return results in this format and so, if other formats are used then the wrapper itself will need to parse them. The result of this parsing must be a PuppyIR response object (for more see: :ref:`puppy_response`), with all the standard fields required by the OpenSearch standard.

For examples of how to do this, consult the code in the following wrappers:

* For JSON parsing: the Guardian and Yahoo! wrappers.
* For XML parsing: the Wikipedia and Simple Wikipedia wrappers.