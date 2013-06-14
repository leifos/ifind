# -*- coding: utf8 -*-

import urllib2
import json

from puppy.search.engine.site import sitesearch
from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class BingV2(SearchEngine, sitesearch):
  """
  Bing search engine wrapper for Version 2.2 of the API - allowing for a large variety of source types to be searched.

  One of the key advantages of using this wrapper is using the new features and also being able to use multiple sources to create a mash-up.
  i.e. source="Web+Image" gets results from the web and also image search services.

  You must include your application's Bing ID in your service manage config to use this service. It should be under the identifier "bing_api_key"

  If you use the 'Spell' source, then you must set the 'market' parameter to match the language you are querying in i.e. English UK set Market to en-gb or Dutch set it to nl-nl

  Parameters:

  * source (str): what source the results should come from, valid options are: Web, News, Video, Image, Spell, RelatedSearch.

  * adult (str):  Strict is the default, not recommended to change this

  * market (str): For UK: en-GB, For Netherlands: nl-NL etc

  * resultsPerPage (int): How many results per page

  -- 'Image' and 'Video' only --
  * filters (str): filter options split up by '+' you can only have one of each type see Bing API documentation for what these are

  -- 'Video' and 'News' only --
  * sortBy (str): sort news by either 'Date' or 'Relevance'

  -- 'News' only --
  * newsCategory (str): what sort of news is wanted - see BingAPI for list of options, for example: 'rt_ScienceAndTechnology'
  """
    
  def __init__(self, service, source = 'Web', adult = 'Strict', market = 'en-GB', resultsPerPage = 8, filters = None, sortBy = None, newsCategory = None, sites=None, **args):
    SearchEngine.__init__(self, service, **args)
    sitesearch.__init__(self, sites)

    self.source = source
    self.adult = adult
    self.market = market
    self.resultsPerPage = resultsPerPage
    self.filters = filters
    self.sortBy = sortBy
    self.newsCategory = newsCategory

  def search(self, query, offset):
    """Search function for Bing V2 Search.
           
    Parameters:
    
    * query (puppy.model.Query)

    * offset (int): result offset for the search
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_bing_json(site, url, query, results, sources, pos):
      """Create a OpenSearch Response from Bing V2 results.
      
      Bing's search API returns results in JSON format. This function simply loads the JSON into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      * sources (array): all the sources we are currently using i.e. Web and News or just Web
      * pos(int): what page we are starting on
      
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
        response.feed.setdefault("opensearch_totalresults", int(results[self.source]['Total']))
        response.feed.setdefault("opensearch_itemsperpage", self.resultsPerPage)
        response.feed.setdefault("opensearch_startindex", pos )
      except KeyError:
        response.feed.setdefault("opensearch_totalresults", 0)
        response.feed.setdefault("opensearch_itemsperpage", 0)
        response.feed.setdefault("opensearch_startindex", 0)
      
      for sourceType in sources: # Go through every source type selected, parse its results and store them. 
        if (sourceType == 'Web') and ('Results' in results['Web']):
          response = parseWebJson(response, results, url)
        elif (sourceType == 'News') and ('News' in results):
          response = parseNewsJson(response, results, url)
        elif (sourceType == 'Image') and ('Results' in results['Image']):
          response = parseImageJson(response, results, url)
        elif (sourceType == 'Video') and ('Results' in results['Video']):
          response = parseVideoJson(response, results, url)
        elif (sourceType == 'Spell') and ('Spell' in results):
         response =  parseSpellJson(response, results, query, url)
        elif (sourceType == 'RelatedSearch') and ('RelatedSearch' in results):
         response = parseRelatedSearchJson(response, results, query, url)
               
      return response

    def parseWebJson(response, results, url):
      """Parses Bing web results and returns them ready to be added to response's entries."""

      for result in results['Web']['Results']:
        try:
          result_dict = {'title': result['Title'], 'link': result['Url'], 'summary': result['Description']}
          result_dict['dateTime'] = result['DateTime'] # Last update to the site/result

          if 'SearchTags' in result:
            result_dict['tags'] = result['SearchTags'] # Tags associated with this result 

          if 'DeepLinks' in result: 
            deepLinks = [] # URL's associated with the main result i.e. news, about etc pages from the result          
            for deepLink in result['DeepLinks']:
              deepLinks.append({'url': deepLink['Url'], 'title': deepLink['Title']})
            
            result_dict['deepLinks'] = deepLinks
          response.entries.append(result_dict)
          
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue

      return response

    def parseNewsJson(response, results, url):
      """Parses Bing news results and returns them ready to be added to response's entries."""

      for result in results['News']['Results']:
        try:
          result_dict = {'title': result['Title'], 'link': result['Url'], 'summary':  result['Snippet']}
          result_dict['datetime'] = result['Date'] # When the news story was posted
          result_dict['breakingNews'] = result['BreakingNews'] # 1 = yes, 0 = no

          if 'RelatedSearches' in result: 
            relatedSearches = [] # Related searches to your query
            for relatedSearch in result['RelatedSearches']:
              relatedSearches.append({'url': relatedSearch['Url'], 'title': relatedSearch['Title']})
            
            result_dict['relatedSearches'] = relatedSearches
        
          if 'NewsCollections' in result: 
            relatedCollections = [] # Related news collections
            for collection in result['NewsCollections']:
              collection_dict = {}
            
              if 'Name' in collection:
                collection_dict['name'] = collection['Name']

              if 'NewsArticles' in collection: # If we have articles in it
                articlesArray = []
                for article in collection['NewsArticles']: # Grab all the related articles in the collection
                  article_dict = {'title': article['Title'], 'link': article['Url']}

                  # The following fields are not always in related collection articles
                  if 'Date' in article:
                    article_dict['date'] = article['Date']

                  if 'Snippet' in article:
                    article_dict['summary'] = article['Snippet']

                  if 'Source' in article:
                    article_dict['source'] = article['Source']

                  articlesArray.append(article_dict)

                collection_dict['articles'] = articlesArray
              
              relatedCollections.append(collection_dict)
            
            result_dict['relatedCollections'] = relatedCollections

          response.entries.append(result_dict)
          
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue

      return response

    def parseImageJson(response, results, url):
      """Parses Bing image results and returns them ready to be added to response's entries."""

      for result in results['Image']['Results']:
        try:
          result_dict = {'title': result['Title'], 'link': result['MediaUrl']}
          result_dict['displayLink'] = result['DisplayUrl'] # Full Resolution Version - normally same as default
          result_dict['sourceLink'] = result['Url'] # Website the image is from
          result_dict['width'] = result['Width']
          result_dict['height'] = result['Height']
          result_dict['summary'] = "Image result for '{0}' from {1}".format(query, 'Bing V2 Search Api')
          result_dict['thumbnail'] = result['Thumbnail']['Url']
          result_dict['thumbnailWidth'] = result['Thumbnail']['Width']
          result_dict['thumbnailHeight'] = result['Thumbnail']['Height']
          response.entries.append(result_dict)
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
                  
      return response

    def parseVideoJson(response, results, url):
      """Parses Bing video results and returns them ready to be added to response's entries."""
      
      for result in results['Video']['Results']:
        try:
          result_dict = {'title':  result['Title'], 'link': result['ClickThroughPageUrl']}
          result_dict['sourceLink'] = result['PlayUrl'] # Original url - with YouTube results this often doesn't work
          result_dict['sourceTitle'] = result['SourceTitle'] # Title of website the video is from
          result_dict['summary'] = "Video result for '{0}' from {1}".format(query, result['SourceTitle'])
          result_dict['thumbnail'] = result['StaticThumbnail']['Url']
          response.entries.append(result_dict)
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
        
      return response

    def parseSpellJson(response, results, query, url):
      """Parses Bing spelling suggestion results and returns them ready to be added to response's entries."""  
         
      for result in results['Spell']['Results']:
        try:
          result_dict = {"title": "Spelling Suggestion for: '{0}'".format(query),  "link": ''}
          result_dict['summary'] = "Original query: '{0}'. Suggested correction of query: '{1}'.".format(query, result['Value']) 
          result_dict['suggestion'] = result['Value']
          response.entries.append(result_dict)
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
        
      return response

    def parseRelatedSearchJson(response, results, query, url):
      """Parses Bing related search results and returns them ready to be added to response's entries."""
      
      for result in results['RelatedSearch']['Results']:
        try:
          result_dict = {"title": result['Title'],  "link": result['Url']}
          result_dict['summary'] = "Search Suggestion of: '{0}' for the original query of: '{1}'.".format(result['Title'], query)
          response.entries.append(result_dict)
        except Exception, e:    # If there is a parsing problem, print out an error and just skip this individual result
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue
        
      return response

    # Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["bing_api_key"]
    except KeyError:
      raise ApiKeyError("Bing V2", "bing_api_key")
	
    # Now that an API key has been supplied, try to get results from the search engine itself
    try:
      formattedQuery = urllib2.quote(self._modify_query(query.search_terms))
      pos = self._origin() + (offset * self.resultsPerPage)

      url = "http://api.search.live.net/json.aspx?Appid={0}&version=2.2&query={1}&sources={2}&market={3}&{2}.count={4}&adult={5}&{2}.offset={6}".format(appId, formattedQuery, self.source, self.market, self.resultsPerPage, self.adult, pos)

      sources = self.source.split('+')

      for sourceType in sources:
        # If we are using the 'Image' or 'Video' source type we can use filtering - i.e. only widescreen images or high res videos
        if((sourceType == 'Image') or (sourceType == 'Video')) and self.filters:
          url += "&{0}.filters={1}".format(self.source, self.filters)

        # If we are sing 'Video' or 'News' we can sort the results
        if ((sourceType == 'Video') or (sourceType == 'News')) and self.sortBy:
          url += "&SortBy={0}".format(self.sortBy)

        # If we are using the 'News' source type we can add the custom news paramters
        if sourceType == 'News' and self.newsCategory:
          url += "&Category={0}".format(self.newsCategory)
    
      data = urllib2.urlopen(url).read()
      results = json.loads(data)
      return parse_bing_json('Bing V2', url, query.search_terms, results['SearchResponse'], sources, pos)

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Bing V2", e, errorType = 'urllib2', url = url)

    # Check for a type error for offset or resultsPerPage
    except TypeError, e:
      note = "Please ensure that 'offset' and 'resultsPerPage' are integers if used"
      if isinstance(offset, int) == False:
        raise SearchEngineError("Bing V2", e, note = note, offsetType = type(offset))

      if isinstance(self.resultsPerPage, int) == False:
        raise SearchEngineError("Bing V2", e, note = note, resultsPerPageType = type(self.resultsPerPage))

      raise SearchEngineError("Bing V2", e, note = note)
	  
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Bing V2", e, url = url)