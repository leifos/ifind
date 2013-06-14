# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search.engine.site import sitesearch
from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class SoundCloud(SearchEngine):
  """
  SoundCliud search engine wrapper for a music sharing application allowing the searching for tracks.

  You must include your api key for Wordnik in your service manage config to use this service. It should be under the identifier "soundcloud_api_key"

  Parameters:

  * resultsPerPage (int): the number of results to return for a search query

  * order (str): the order to return results in, valid values are 'created_at' and 'hotness' (this later one being popularity of tracks)

  * tags (str): a comma separated string of tags to look for along with the query

  * filter (str): filter via the access category, valid values are: 'all', 'public', 'private', 'streamable', 'downloadable'

  * genres (str):  a comma separated string of genres to look for along with the query (see the SoundCloud site for a list of genres)

  * types (str): a comma separated string of types of track to look for along with the query (see the SoundCloud site for a list of types - examples are 'live' or 'demo')

  * bpmFilter (dict): filters via beats per minute, with the fields being 'from' and 'to' their values both being ints

  * durationFilter (dict): filters via duration of the track, with the fields being 'from' and 'to' their values both being ints with the units being milliseconds

  * createdFilter (dict): filters via when the track was created, with the fields being a string of format: 'yyyy-mm-dd hh:mm:ss'

  """
    
  def __init__(self, service, resultsPerPage = 8, order=None, tags=None, filter=None, genres=None, types=None, bpmFilter=None, durationFilter=None, createdFilter=None, **args):
    SearchEngine.__init__(self, service, **args)

    self.resultsPerPage = resultsPerPage
    self.order = order
    self.tags = tags
    self.filter = filter
    self.genres = genres
    self.types = types
    self.bpmFilter = bpmFilter
    self.durationFilter = durationFilter
    self.createdFilter = createdFilter

  def search(self, query, offset):
    """
    Search function for SoundCloud Search.        
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_soundcloud_json(site, query, results, url, offset):
      """      
      SoundCloud's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
      * offset (int): which page of results we are retrieving
      
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
        response.feed.setdefault("opensearch_itemsperpage", self.resultsPerPage)
        response.feed.setdefault("opensearch_totalresults", int(len(results)))
        response.feed.setdefault("opensearch_startindex", 0)
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      # There is no pagination as a parameter, all results are simple returned in one, so this mimics pagination
      startIndex = offset * self.resultsPerPage

      if (startIndex + self.resultsPerPage) > len(results):
        endIndex = len(results)
      else:
        endIndex = startIndex + self.resultsPerPage

      # Go through a subset of the results and grab them - corresponding to the page in question
      for i in range(startIndex, endIndex):
        try:
          result_dict = results[i]
          result_dict['summary'] = results[i]['description']
          result_dict['link'] = results[i]['permalink_url']
          result_dict['artist'] = results[i]['user']['username']
          response.entries.append(result_dict)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      
      return response        

    # Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      apiKey = self.service.config["soundcloud_api_key"]
    except KeyError:
      raise ApiKeyError("SoundCloud Search API", "soundcloud_api_key")
	
    try:
      url = "http://api.soundcloud.com/tracks.json?client_id={0}&q={1}".format(apiKey, urllib2.quote(query.search_terms))

      if self.order: # If we have set a non default ordering of results
        url += "&order={0}".format(self.order)

      if self.tags: # If we have defined tags to search for along with the query
        url += "&tags={0}".format(self.tags)
	
      if self.filter: # If we are filtered based on public, private, streamable etc
        url += "&filter={0}".format(self.filter)
		
      if self.genres: # If we are filtering by genre
        url += "&genres={0}".format(self.genres)
			
      if self.types: # If we are filtering by type i.e. demo etc
        url += "&types={0}".format(self.types)

      # If we are filtering by bpm, beats per minute, with a minimum value
      if (self.bpmFilter) and ('from' in self.bpmFilter):
        url += "&bpm[from]={0}".format(self.bpmFilter['from'])

      # If we are filtering by bpm, beats per minute, with a maximum value
      if (self.bpmFilter) and ('to' in self.bpmFilter):
        url += "&bpm[to]={0}".format(self.bpmFilter['to'])

      # If we are filtering by duration with a minimum value
      if (self.durationFilter) and ('from' in self.durationFilter):
        url += "&duration[from]={0}".format(self.durationFilter['from'])

      # If we are filtering by duration with a maximum value
      if (self.durationFilter) and ('to' in self.durationFilter):
        url += "&duration[to]={0}".format(self.durationFilter['to'])

      # If we are filtering by creation date with a minimum value
      if (self.createdFilter) and ('from' in self.createdFilter):
        url += "&created_at[from]={0}".format(self.createdFilter['from'])

      # If we are filtering by creation date with a maximum value
      if (self.createdFilter) and ('to' in self.createdFilter):
        url += "&created_at[to]={0}".format(self.createdFilter['to'])

      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_soundcloud_json('SoundCloud Search API', query.search_terms, results, url, offset)

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("SoundCloud Search API", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'resultsPerPage' and 'offset' are integers if used"

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("SoundCloud Search API", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      if isinstance(offset, int) == False:
        raise SearchEngineError("SoundCloud Search API", e, note = note, offsetType = type(offset))

      raise SearchEngineError("SoundCloud Search API", e, url = url)
      
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("SoundCloud Search API", e, url = url)