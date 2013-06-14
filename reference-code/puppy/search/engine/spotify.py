# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class Spotify(SearchEngine):
  """
  Spotify search engine.

  Parameters:

  * source (str):  what sort of results should be returned, the options are: 'tracks', 'albums', 'artists'
  """
    
  def __init__(self, service, source = 'tracks', **args):
    super(Spotify, self).__init__(service, **args)
    self.source = source

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Spotify """
    return 1
    
  def search(self, query, offset):
    """Search function for Spotify Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_spotify_json(site, url, query, results):
      """      
      Spotify's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
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
        response.feed.setdefault("opensearch_totalresults", int(results['info']['num_results']))
        response.feed.setdefault("opensearch_itemsperpage", int(results['info']['limit']))
        response.feed.setdefault("opensearch_startindex", int(results['info']['page']))
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      if (self.source == 'tracks') and ('tracks' in results):
        response = parse_tracks_json(response, results, url)
      elif (self.source == 'albums') and ('albums' in results):
        response = parse_albums_json(response, results, url)
      elif (self.source == 'artists') and ('artists' in results):
        response = parse_artists_json(response, results, url)
      
      return response

    def parse_tracks_json(response, results, url):
      """This method parses the JSON for track results."""
      for result in results['tracks']:
        try:
          track_dict = {'title': result['name'], 'link': result['href'], 'length': result['length']}
          track_dict['trackNumber'] = result['track-number']

          artists = []
          for artist in result['artists']:
            artists_dict = {'name': artist['name']}

            if 'href' in artist:
              artists_dict['link'] = artist['href']

            artists.append(artists_dict)

            track_dict['artists'] = artists
            track_dict['album'] = {'name': result['album']['name'], 'year': result['album']['released'], 'link': result['album']['href']}
            track_dict['summary'] = "{0} from {1}".format(track_dict['title'], result['album']['name'].encode('ascii', 'ignore'))
            track_dict['popularity'] = result['popularity']
            response.entries.append(track_dict)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      return response

    def parse_albums_json(response, results, url):
      """This method parses the JSON for album results."""
      for result in results['albums']:
        try:
          album_dict = {'title': result['name'], 'link': result['href'], 'summary': '', 'popularity': result['popularity']}

          artists = []
          for artist in result['artists']:
            artists_dict = {'name': artist['name']}

            if 'href' in artist:
              artists_dict['link'] = artist['href']

            artists.append(artists_dict)

          album_dict['artists'] = artists
          response.entries.append(album_dict)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      return response

    def parse_artists_json(response, results, url):
      """This method parses the JSON for artist results."""
      for result in results['artists']:
        try:
          response.entries.append({'title': result['name'], 'link': result['href'], 'summary': '', 'popularity': result['popularity']})
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
      return response

    try:    
      pos = self._origin() + offset
      serviceName = self.source[:len(self.source) - 1]
      url = "http://ws.spotify.com/search/1/{0}.json?q={1}&page={2}".format(serviceName, urllib2.quote(query.search_terms), pos) 
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_spotify_json('Spotify', url, query.search_terms, results)

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Spotify", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset
    except TypeError, e:
      if isinstance(offset, int) == False:
        note = "Please ensure that 'offset' is an integer."
        raise SearchEngineError("Spotify", e, note = note, offsetType = type(offset))

      raise SearchEngineError("Spotify", e, url = url)
	
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Spotify", e, url = url)