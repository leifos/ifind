# -*- coding: utf8 -*-

import urllib2
from urlparse import urlparse
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
# replace BS parsing with lxml

from puppy.search import SearchEngine
from puppy.model import Query, Response

from puppy.search.exceptions import SearchEngineError

class OpenSearch(SearchEngine):
  """OpenSearch search engine."""
  
  def __init__(self, service, url, **args):
    self.url = url
    self.template = None
    self.results = True
    self.xml = True 
    super(OpenSearch, self).__init__(service, **args)
    
  
  def discover_description(self):
    """
    Discover if website supports OpenSearch.
    
    Finds a <link rel='search'> pattern for the given url.  
    TODO: there are no rules about whether the OpenSearch Description document is linked using an absolute or relative path.  
    Therefore, only a simple test is used here to determine if the link starts with 'http://'.
        
    Returns:
    
    * address of OpenSearch description document (str)
    
    Raises:
    
    * Exception: if website does not appear to support OpenSearch
    * urllib2.URLError: if website cannot be reached
    """
    
    try:
      user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
      headers = {'User-Agent': user_agent}
      request = urllib2.Request(self.url, headers=headers)
      response = urllib2.urlopen(request)
      os_link = BeautifulSoup(response.read()).find('link', rel='search')
      if os_link == None:
        raise Exception("{0} does not support OpenSearch".format(self.url))
      elif os_link.attrMap.has_key('type'):
        if os_link.attrMap['type'] == "application/opensearchdescription+xml":
          if os_link.attrMap['href'][0:4] == 'http':
            return os_link.attrMap['href']
          else:
            parsed = urlparse(self.url)
            scheme, netloc = parsed.scheme, parsed.netloc
            return "".join((scheme, '://', netloc, os_link.attrMap['href']))
        else:
          raise Exception("{0} does not support OpenSearch".format(self.url))
      else:
        raise Exception("{0} does not support OpenSearch".format(self.url))
    except urllib2.URLError, e:
      print "Could not retrieve {0}: {1}".format(self.url, e)
  
  
  def find_template(self, url):
    """
    Find search pattern from OpenSearch Description document.
    
    Each OpenSearch Description document has a template that tells a client how to perform a search.  
    This function searches for the <url> tag and returns the template attribute.
    
    Parameters:
    
      * url (str): address of the OpenSearch Description document
    
    Returns:
    
      * str: search template
    
    Raises:
    
      * urllib2.URLError: if website cannot be reached
    """
    try:
      user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
      headers = {'User-Agent': user_agent}
      request = urllib2.Request(url, headers=headers)
      response = urllib2.urlopen(request).read()
      if BeautifulStoneSoup(response).find('url', type="application/rss+xml"):
        os_url = BeautifulStoneSoup(response).find('url', type="application/rss+xml")
      elif BeautifulStoneSoup(response).find('url', type="application/x-suggestions+xml"):
        os_url = BeautifulStoneSoup(response).find('url', type="application/x-suggestions+xml")
        self.results = False
      elif BeautifulStoneSoup(response).find('url', type="application/x-suggestions+json"):
        os_url = BeautifulStoneSoup(response).find('url', type="application/x-suggestions+json")
        self.results = False
        self.xml = False
      return os_url.attrMap['template']
    except urllib2.URLError, e:
      print "Could not retrieve OpenSearch Description from {0}: {1}".format(url, e)
  
  
  def search(self, query, pos=0):
    """Search function for OpenSearch compliant website.
    
    If a template exists, a search will be executed immediately using the search template,
    Otherwise, given the site URL, a template will attempt to be discovered.
    
    Parameters:
    
    * query (puppy.model.Query)
    * pos (int)
    
    Returns:
    
    * results (puppy.model.Response)
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    if self.template:
      # template exists, use it to search
      search_url = self.template.replace('{searchTerms}', urllib2.quote(query.search_terms))
      if (pos != 0):
        search_url = search_url.replace('{start}', urllib2.quote(pos))
      else:
        pass
      try:
        response = urllib2.urlopen(search_url).read()
        if self.results and self.xml:
          return Response.parse_feed(response)
        elif not self.results and self.xml:
          return Response.parse_xml_suggestions(response)
        elif not self.results and not self.xml:
          return Response.parse_json_suggestions(response)
      except urllib2.URLError, e:
        print "Opensearch for {0} failed".format(self.url)      
    else:
      # attempt to discover template
      try:
        # assign template and search
        self.template = self.find_template(self.discover_description())
        return self.search(query, pos)

      # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
      except urllib2.URLError, e:
        raise SearchEngineError("'{0}' with OpenSearch Wrapper".format(self.url), e, errorType = 'urllib2')