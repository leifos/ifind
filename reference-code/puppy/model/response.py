# -*- coding: utf8 -*-

import feedparser
import json


class Response(object):
  """
  Data model for search results.  Response has four main attributes:
  
  * feed: dictionary of information about the search results {title,
    * description, etc}

  * entries: list of search results [{title, link, summary, etc}, ...]

  * namespaces: list of namespaces ["http://a9.com/-/spec/opensearch/1.1/",
    * ...]

  * version: source type of orginal results "rss/atom/json"

  """
  def __init__(self, results={}):
    """Constructor for Response."""
    super(Response, self).__init__()
    self.feed = results['feed'] if results.has_key('feed') else {}
    self.entries = results['entries'] if results.has_key('entries') else []
    self.namespaces = results['namespaces'] if results.has_key('namespaces') else {}
    self.version = results['version'] if results.has_key('version') else ""
  
  
  def __str__(self):
    return str({"entries": self.entries, "feed": self.feed, "namespaces": self.namespaces, "version": self.version})  
  
  
  @staticmethod  
  def parse_feed(xml_feed):
    """Parses a RSS/ATOM feed of Opensearch results"""
    response = Response(feedparser.parse(xml_feed))
    # in some cases, feedparser does not add the required result fields
    # in these cases, empty strings are inserted
    for result in response.entries:
      result.setdefault('title', '')
      result.setdefault('summary', '')
      result.setdefault('link', '')
    return response
  
  
  @staticmethod
  def parse_xml_suggestions(xml_doc):
    """Parse a XML document of Opensearch suggestions"""

    from lxml import etree
    response = Response()
    response.feed.setdefault("title", "Search Suggestions")
    response.namespaces.setdefault("searchsuggest", "{http://opensearch.org/searchsuggest2}")
    response.version = 'xml'
    
    root = etree.XML(xml_doc)
    ns = response.namespaces["searchsuggest"]
    section = root.find("{0}Section".format(ns))
    items = section.findall("{0}Item".format(ns))
    
    for item in items:
      # TODO: parse additional metadata (e.g. wikipedia includes thumbnails)
      title = item.find("{0}Text".format(ns)).text
      summary = item.find("{0}Description".format(ns)).text
      link = item.find("{0}Url".format(ns)).text
      response.entries.append({'title': title, 'summary': summary, 'link': link})    
    
    return response
  
  @staticmethod
  def parse_json_suggestions(json_doc):
    """Parse a JSON document of Opensearch suggestions"""
    print "json parsing"
    response = Response()
    response.feed.setdefault("title", "Search Suggestions")
    response.namespaces.setdefault("searchsuggest", "{http://opensearch.org/searchsuggest2}")
    response.version = 'json'
    
    items = json.loads(json_doc)[1]
    for item in items:
      response.entries.append({'title': item})
    
  
  def to_rss(self):
    """
    Creates an RSS feed from a Response object.
    
    Returns:
    
    * response_xml (str): Response as RSS feed
    """
    pass
  
  
  def to_atom(self):
    """
    Creates an XML from a OpenSearch Response.
    
    Returns:
    
    * response_xml (str): OpenSearch Response as an ATOM feed
    """
    pass
  
  
  def to_json(self):
    """
    Creates JSON from a Response object.
    
    Returns:
    
    * response_json (str): Response as JSON
    """
    # minor hack: feed parser included a date object which json does not handle
    if self.feed.has_key("updated_parsed"):
      self.feed['updated_parsed'] = str(self.feed['updated_parsed'])
    
    for entry in self.entries:
      if entry.has_key('updated_parsed'):
        entry['updated_parsed'] = str(entry['updated_parsed'])
      if entry.has_key('published_parsed'):
        entry['published_parsed'] = str(entry['published_parsed'])
    
    return json.dumps({"entries":self.entries, "feed": self.feed, "namespaces": self.namespaces, "version": self.version})
  
  
  def get_totalresults(self):
    """
    Returns the number total of results, as reported by the search engine.
    
    This number is used mainly by page algorithms.
    
    Returns:
    
    * opensearch_totalresults: the total_results value
    """
    if self.feed.has_key('opensearch_totalresults'):
      return int(self.feed['opensearch_totalresults'])
    if self.feed.has_key('os_totalresults'):
      return int(self.feed['os_totalresults'])
    return 0
    
  
  def get_itemsperpage(self):
    """
    Returns the number of results per page, as reported by the search engine (usually, 10, except for Google, 8)
    
    This number is used mainly by page algorithms.
    
    Returns:
    
    * opensearch_itemsperpage: the itemsperpage value
    """
    if self.feed.has_key('opensearch_itemsperpage'):
      return int(self.feed['opensearch_itemsperpage'])
    if self.feed.has_key('os_itemsperpage'):
      return int(self.feed['os_itemsperpage'])    
    return 0
    
  
  def get_startindex(self):
    """
    Returns the start item for the current "page", as reported by the search engine. It is usually 0 or items per page * page number
    
    This number is used mainly by page algorithms.
    
    Returns:
    
    * opensearch_startindex: the startindex value
    """
    if self.feed.has_key('opensearch_startindex'):
      return int(self.feed['opensearch_startindex'])
    if self.feed.has_key('os_startindex'):
      return int(self.feed['os_startindex'])
    return 0  
    
  
