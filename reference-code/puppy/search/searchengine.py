# -*- coding: utf8 -*-

import urllib2

class SearchEngine(object):
  """Abstract search engine interface."""
  
  def __init__(self, service, **args):
    """
    Constructor for SearchEngine.
    
    Parameters:
    
    * service (puppy.service.SearchService/puppy.pipeline.PipelineService): A reference to the parent search service
    * options (dict) a dictionary of engine specific options - handled by derived classes
    * args: any additional invalid options that were added that the dervived clases don't handle
    """
    self.name = self.__class__.__name__
    self.service = service
    self.handleException = True  # If it fails should it fail gracefully or raise an exception (default) in Search Service?
    self.configure_opener()

    # Prints invalid parameters recieved by the Search Engine Wrapper - this allows the developer's code not to crash and alerts them to their mistake
    for parameter in args:
      print "{0} recieved invalid parameter called: {1}.\nPlease consult the API reference document for a list of valid parameters.".format(self.name, parameter)

  def _origin(self):
    """ This defines the default origin (0-indexed) for results retrieved from a search engine."""
    return 0
  
  
  def configure_opener(self):
    """Configure urllib2 opener with network proxy if one has been added to the parent services config dictionary"""
    
    if "proxyhost" in self.service.config:
      proxy_support = urllib2.ProxyHandler({'http': self.service.config["proxyhost"]})
      opener = urllib2.build_opener(proxy_support)
    else:
      opener = urllib2.build_opener()
      
    urllib2.install_opener(opener)
    
  
  def search(self, query, offset=0):
    """
    Perform a search, retrieve the results and process them into the response format.
    
    N.B. This should be implemented in the derived classes.
    
    Parameters:
    
    * query (puppy.model.Query): query object
    * offset (int): result offset
    
    Returns:
      
    * results (puppy.model.Response): results of the search
    
    """
    pass