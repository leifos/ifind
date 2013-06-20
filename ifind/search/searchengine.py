__author__ = 'leifos'

# -*- coding: utf8 -*-

import urllib2
from ifind.search.response import Response
from ifind.search.query import Query

class SearchEngine(object):
  """Abstract search engine interface."""

  def __init__(self, proxy_host=None, api_key=None, **kwargs):
    """
    Constructor for SearchEngine.

    Parameters:
        * kwargs: any additional invalid options that were added that the dervived clases don't handle
    """

    self.name = self.__class__.__name__
    self.handleException = True  # If it fails should it fail gracefully or raise an exception (default) in Search Service?
    self.proxy_host = proxy_host
    self.api_key = api_key

    self.configure_opener()


  def _origin(self):
    """ This defines the default origin (0-indexed) for results retrieved from a search engine."""
    return 0


  def configure_opener(self):
    """Configure urllib2 opener with network proxy if one has been added to the parent services config dictionary"""

    if self.proxy_host:
      proxy_support = urllib2.ProxyHandler({'http': self.proxy_host})
      opener = urllib2.build_opener(proxy_support)
    else:
      opener = urllib2.build_opener()

    urllib2.install_opener(opener)


  def search(self, query):
    """
    Perform a search, retrieve the results and process them into the response format.

    N.B. This should be implemented in the derived classes.

    Parameters:

    * query (ifind.search.Query): query object

    Returns:

    * results (ifind.search.Response): results of the search

    """
    pass