# -*- coding: utf8 -*-

import urllib2
import json
from math import atan2, sin, cos, sqrt, radians

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class GoogleGeocode(SearchEngine):
  """
  GoogleGeocode search service.

  Parameters:

  * sensor(str): does your device have a GPS sensor or not, not recommended to change from 'false' but the other option is, naturally, 'true' - must be lowercase

  """
    
  def __init__(self, service, sensor = 'false', **args):
    super(GoogleGeocode, self).__init__(service, **args)
    self.sensor = sensor

  def calcDistance(self, lat1, lat2, lon1, lon2):
    # Credit for this method: http://www.movable-type.co.uk/scripts/latlong.html - modified by Doug for Python
    radiusEarth = 6371; # approx in km
    dLat = radians(lat2-lat1)
    dLon = radians(lon2-lon1)
    self.lat1 = radians(lat1)
    self.lat2 = radians(lat2)

    a = sin(dLat/2) * sin(dLat/2) + sin(dLon/2) * sin(dLon/2) * cos(lat1) * cos(lat2); 
    c = 2 * atan2(sqrt(a), sqrt(1-a)); 
    distance = radiusEarth * c;

    return distance  
    
  def search(self, query, offset):
    """Search function for Google Geocode Search.
        
    
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_geocode_json(site, url, query, results):
      """Create a OpenSearch Response from Google Geoode results results.
      
      Google's Geocode search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
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
      response.feed.setdefault("opensearch_startindex", 0)
      
      for result in results:
        try:
          resultDict ={}
          resultDict['title'] = result['formatted_address']
          longTitle = ''
          for component in result['address_components']:
            longTitle += (component['long_name'] + ', ')
          resultDict['link'] = ''
          resultDict['longTitle'] = longTitle[:len(longTitle)-2]
          resultDict['lat'] = result['geometry']['location']['lat']
          resultDict['lon'] = result['geometry']['location']['lng']
       
          if 'bounds' in result['geometry']:
            resultDict['neBorderLat'] = result['geometry']['bounds']['northeast']['lat']
            resultDict['neBorderLon'] = result['geometry']['bounds']['northeast']['lng']
            resultDict['swBorderLat'] = result['geometry']['bounds']['southwest']['lat']
            resultDict['swBorderLon'] = result['geometry']['bounds']['southwest']['lng']
            resultDict['distanceAcross'] = self.calcDistance(resultDict['neBorderLat'], resultDict['swBorderLat'], resultDict['neBorderLon'], resultDict['swBorderLon'])
            resultDict['summary'] = "{0} is found at: Latitude: {1}, Longitude: {2}. The area it covers is {3}km across (between the NE and SW corners).".format(resultDict['title'], resultDict['lat'], resultDict['lon'], resultDict['distanceAcross'])
          else:
            resultDict['summary'] = "{0} is found at: Latitude: {1}, Longitude: {2}.".format(resultDict['title'], resultDict['lat'], resultDict['lon'])
          response.entries.append(resultDict)

        # If there is an arithmetic error pass on the result but note it for the user and the result in question
        except ArithmeticError, e:
          note =  "Arithmetic Error occured when calculating the distance across for a result."
          print "An {0}\nResult: {1}\n\n".format(note, result)
          continue
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue

      # If the processing worked okay then set total results and items per page
      response.feed['opensearch_totalresults'] = len(response.entries)
      response.feed['opensearch_itemsperpage'] = len(response.entries)
      return response

    try:
      url = "https://maps.googleapis.com/maps/api/geocode/json?address={0}&sensor={1}".format(urllib2.quote(query.search_terms), self.sensor)   
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_geocode_json('Google Geocode', url, query.search_terms, results['results'])
    
    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Google Geocode", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or a generic type error if offset is valid
    except TypeError, e:
      if isinstance(offset, int) == False:
        note = "Please ensure that 'offset' is an integer."
        raise SearchEngineError("Google Geocode", e, note = note, offsetType = type(offset))

      raise SearchEngineError("Google Geocode", e, url = url)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Google Geocode", e, url = url)