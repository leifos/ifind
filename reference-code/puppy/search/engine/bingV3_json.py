# -*- coding: utf8 -*-
# coding=utf-8
'''
BingV3 Search Wrapper using the JSON response format.

Implementation notes
====================

(1) Site search is back, couldn't get the old style back so implemented it from scratch
    using regular expressions to extract only the domain from our URLS (since this is how
    the Bing query language works) and augment the query accordingly.
(2) All the parameters etc we had before are here and present as before.
(3) I've added a little more validation now taking into account if it's a valid source type
    and also if the results per page setting is valid (not checking it's type though).
(4) Unlike before, I've done a more graceful parsing style: there's only one parser for all sources
    and it takes a JSON result (doesn't matter the source) and a mapping of Puppy to Bing keys.
    It then attempts to set values for all our Puppy keys, in the result, and, failing that, just
    sets a blank value and outputs a warning to the console.
    
    Did it so the mapping is an array of keys and made a simple parser to go through and check
    if the keys are there at each level until either it finds the last key (thus selecting the value)
    or fails to find a key, in which case a blank value will be set and a warning outputted to console.
(5) Spelling suggestions for some reason are not implemented in JSON, not elegant but I'm just matching
    the suggestions using regular expressions from the raw response.

Created by Douglas Dowie, 16th-17th August 2012 (based on BingV2 and Leif's BingV3 wrapper)
'''
# PuppyIR Imports
from puppy.search.exceptions import SearchEngineError, ApiKeyError
from puppy.search import SearchEngine
from puppy.model import Response

# Python Imports
import urllib, urllib2
import json             # For processing JSON responses
import re               # For my hacky matching of spelling suggestions from Atom Feeds

class BingV3_json(SearchEngine):   

    def __init__(self, service, source = 'Web', adult = 'Strict', market = 'en-US', resultsPerPage = 8, filters = None, sortBy = None, newsCategory = None, sites=None, **args):
        """
        Arguments for all source types:
            (1) source(str)         -    Should be 'Web', 'Image', 'News', 'RelatedSearch', 'SpellingSuggestions'
            (2) adult(str)          -    Strict is the default, not recommended to change this, can also be 'Moderate' or 'Off'
            (3) market(str)         -    For UK: en-GB, For Netherlands: nl-NL etc
            (4) resultsPerPage(int) -    How many results per page
            
        Arguments for Image and Video searches only:
            (1) filters(str)        -    Filter options split up by '+' you can only have one of each type see 
                                         Bing API documentation for examples of the valid filters.
                                         
                                         Example: "Style:Photo+Aspect:Tall'" gets tall photos.
                                     
        Arguments for Video and News searches only:
            (1) sortBy(str)         -    You can select to sort by either 'Date' or 'Relevance'

        Arguments for News searches only:
            (1) newsCategory(str)   -    What sort of news is wanted, see BingAPI for list of options, for example:
                                         'rt_ScienceAndTechnology' to find news under this category. Only available
                                         with the en-US market, 'cause the rest of the world do not like categories.
        """
        SearchEngine.__init__(self, service, **args)    # This will also handle any unsupported parameters
        
        # The search sources have different limits
        sources_to_limits = {"Image"                :   50,
                             "Web"                  :   50,
                             "News"                 :   15,
                             "RelatedSearch"        :   50,
                             "Video"                :   50,
                             "SpellingSuggestions"  :   50}
        
        self.engineName = "Bing V3_json"            # Used for error identification  
        
        # If there is not entry in the sources dictionary with their limits raise an Error
        if source in sources_to_limits:        
            self.source = source
        else:
            raise SearchEngineError(self.engineName, "Invalid source type: %s is not supported" % source)
        
        # For some reason Spelling Suggestions (named wrongly in their documentation) is only available as Atom
        if self.source != "SpellingSuggestions":
            self.format = "json"
        else:
            self.format = "atom"
        
        # Quick bit of validation, if greater than the sources limit or 0 or less use a default
        if resultsPerPage > sources_to_limits[source] or resultsPerPage <= 0:
            self.resultsPerPage = 8
        else:
            self.resultsPerPage = resultsPerPage
        
        self.adult = adult
        self.market = market
        self.filters = filters
        self.sortBy = sortBy
        self.newsCategory = newsCategory
        self.sites = sites       
        
    def search(self, query, offset):
        """"Search function for the Microsoft BingV3 wrapper, takes a query and returns a response"""            
        username = ""
        try:
            appId = self.service.config["bing_api_key"]
        except KeyError:
            raise ApiKeyError(self.engineName, "bing_api_key")
        
        query_terms = query.search_terms
        
        # If we have defined specific sites to search for then augment our query
        if self.sites:
            query_terms = self._create_site_search_query(query_terms)

        # REMEMBER: use apostrophes within the string, this is what Bing expects
        queryBingFor = "'"+ query_terms +"'"
        quoted_query = urllib.quote(queryBingFor)
        
        searchURL = self._construct_search_request(quoted_query, offset)

        # Add the API key to the password manager
        password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        password_mgr.add_password(None, searchURL, username, appId)

        # Prepare an authentication handler and open the URL, then load the JSON and send it to the parser
        try:
            handler = urllib2.HTTPBasicAuthHandler(password_mgr)
            opener = urllib2.build_opener(handler)
            urllib2.install_opener(opener)
            
            raw_response = urllib2.urlopen(searchURL).read().decode('utf-8', 'ignore')    # Hacky, sorry
            
            if self.source != "SpellingSuggestions": 
                bing_response = json.loads(raw_response)['d'] # They enclose all JSON results in d for some reason
            else:
                bing_response = str(raw_response)
            
            return self._parse_bing_response(query, bing_response, offset)

        except urllib2.URLError, e:
            raise SearchEngineError(self.engineName, e, errorType = 'urllib2', url = searchURL)
        
        except UnicodeEncodeError, e:
            raise SearchEngineError(self.engineName, e, errorType = 'UnicodeEncodeError', url = searchURL)
        
    def _create_site_search_query(self, query_terms):
        """If we have defined specific sites to search using augment the query accordingly"""
        def get_domain(domain_regex, site):
            # Match the domain and the deeplink if specified            
            domain_deeplink = re.search(domain_regex, site)
            
            # If we matched nothing either my regex needs amended or we gave something invalid
            if not domain_deeplink:
                print "Failed to match the domain plus deeplink from %s" % site
                return None
            else:
                # Get the domain and deeplink, we're going to get rid of the deeplink part
                domain = domain_deeplink.group("domain_deeplink")
                
                # If we have a URL like bbc.co.uk/news then drop the news part
                if "/" in domain:
                     domain = domain.split("/")[0]
                  
                # If we have GET parameters drop them   
                if "?" in domain:
                    domain = domain.split("?")[0]
                    
                return domain
            
        domains  = []
        domain_regex = re.compile(r'(?:http|HTTP)?(?:s|S)?(?:://)?(?:(?:www|WWW)\.)?(?P<domain_deeplink>[\w,\.,\/,?,=,&,\-]*)')
        for site in self.sites:
            domain = get_domain(domain_regex, site)
            
            if domain: domains.append(domain)

        # Edge case, fails to match any domains ignore the sites
        if len(domains) == 0:
            return query_terms
        
        all_sites = " ("
        
        for domain_num , domain in enumerate(domains):
            all_sites += "site: %s" % domain
            
            if domain_num == len(domains) - 1:
                all_sites += ")"
            else:
                all_sites += " OR "
        
        query_terms += all_sites
        
        return query_terms        
        
    def _construct_search_request(self, query, offset):
        """Construct our search URL"""
         # Create the API URL
        rootURL = "https://api.datamarket.azure.com/Bing/Search/"
        
        if self.source != "SpellingSuggestions":        
        
            searchURL = "%s%s?$format=%s&$top=%d&$skip=%d&Query=%s" % (rootURL, self.source, self.format, self.resultsPerPage, offset, query)
            
            # If we've selected a source that allows filters and we added a filter add them
            if self.source in ["Image", "Video"] and self.filters:
                searchURL += "&%sFilters='%s'" % (self.source, self.filters)
                
            # If we've selected a source that allows sorting add our selection
            if self.source in ["News", "Video"] and self.filters:
                searchURL += "&%sSortBy='%s'" % (self.source, self.sortBy)
                
            # They only allow news sorting in the US market, for some reason
            if self.source == "News" and self.market == "en-US" and self.newsCategory:
                searchURL += "&NewsCategory='%s'" % self.newsCategory
    
        else:
            searchURL = "%s%s?$top=%d&Query=%s" % (rootURL, self.source, self.resultsPerPage, query)

        # Add in the market
        searchURL += "&Market='%s'" % self.market
            
        # Adult content filtering
        searchURL += "&Adult='%s'" % self.adult     
            
        return searchURL
    
    def _parse_bing_response(self, query, results, offset):
        """Handles processing the JSON into a PuppyIR Response"""
        response = Response()
        response.version = 'json'
        response.feed.setdefault('title', "Results from %s for: %s" % (self.engineName, query.search_terms))
        response.feed.setdefault('link', "")
        response.feed.setdefault('description', "%s results from %s" % (self.source, self.engineName))
        response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
        
        
        if self.source == "Web":
            entries = self._parse_web_results(results) 
                           
        elif self.source == "Image":
            entries = self._parse_image_results(query, results)
                
        elif self.source == "News":
            entries = self._parse_news_results(results)
                
        elif self.source == "RelatedSearch":
            entries = self._parse_related_results(query, results)
                
        elif self.source == "Video":
            entries = self._parse_video_results(query, results)
                
        elif self.source == "SpellingSuggestions":
            entries = self._parse_spelling_results(query, results)
                
        for entry in entries:
            response.entries.append(entry)
        
        response.feed.setdefault('opensearch_totalresults', len(entries))
        response.feed.setdefault('opensearch_startindex', offset)
        response.feed.setdefault('opensearch_itemsperpage', self.resultsPerPage)

        return response    
    
    # ========================== Parsers for all the various result formats ==========================
    
    def _result_parser(self, result, puppy_to_bing_keys):
        """Parse an individual result and try to match up the keys to construct a dictionary"""
        result_dict = {}
            
        # Iterate through all the keys, checking if there's present in our result
        for puppy_key in puppy_to_bing_keys:            
            # An array of how to match the key, if it's there
            bing_keys = puppy_to_bing_keys[puppy_key]
            
            # Method 1: We just have one entry, just a simple lookup, no need for parsing
            if len(bing_keys) == 1:
                bing_key = bing_keys[0]
                
                if bing_key in result:
                    result_dict[puppy_key] = result[bing_key]
                else:
                    print "Failed to match: %s so added a blank value" % bing_key
                    result_dict[puppy_key] = ""
                 
            # Method 2: we have to check for the presence of each key at each level, simple dumb tree traversal   
            else:
                # We start at the top level, the result itself
                parser_pos = result
                found = False
                for key_num, bing_key in enumerate(bing_keys):  # Go through each key to traverse the result
                    if bing_key in parser_pos:                  # If the key is there do checks               
                        if key_num == len(bing_keys) - 1:       # At the end, we've found our value
                            found = True
                        
                        parser_pos = parser_pos[bing_key]       # Now, either our value or the next level in the result
                    else:
                        break                                   # Stop searching if a key is not found at any stage
                    
                if found == True:
                    result_dict[puppy_key] = parser_pos         # The parser should be on the value now
                else:
                    print "Failed to match a key defined by an array so added a blank value"
                    print bing_keys
                    result_dict[puppy_key] = ""                    
                
        return result_dict        
    
    def _parse_image_results(self, query, response):
        """Go through and parse all the image results from the JSON response"""
        image_results = []
        
        for result in response['results']:
            # Using the old names for backwards compatibility        
            puppy_to_bing_keys = {"title"           :   ["Title"],
                                  "link"            :   ["MediaUrl"],
                                  "displayLink"     :   ["MediaUrl"],
                                  "sourceLink"      :   ["SourceUrl"],
                                  "width"           :   ["Width"],
                                  "height"          :   ["Height"],
                                  "type"            :   ["ContentType"],
                                  "size"            :   ["FileSize"],
                                  "displayUrl"      :   ["DisplayUrl"],
                                  "thumbnail"       :   ["Thumbnail", "MediaUrl"],
                                  "thumbnailWidth"  :   ["Thumbnail", "Width"],
                                  "thumbnailHeight" :   ["Thumbnail", "Height"],
                                  "thumbnailSize"   :   ["Thumbnail", "FileSize"],
                                  "thumbnailType"   :   ["Thumbnail", "ContentType"]}
            
            image_result = self._result_parser(result, puppy_to_bing_keys)
            
            # There is no such field so just adding the query and that it's an image result
            image_result['summary'] = "Image result from a query for %s" % query.search_terms
            
            image_results.append(image_result)  
              
        return image_results
    
    def _parse_web_results(self, response):
        """Go through and parse all the web results from the JSON response"""
        web_results = []
        
        for result in response['results']:
            puppy_to_bing_keys = {"title"           :   ["Title"],
                                  "link"            :   ["Url"],
                                  "summary"         :   ["Description"],
                                  "display_url"     :   ["DisplayUrl"]}
            
            web_result = self._result_parser(result, puppy_to_bing_keys)
            web_results.append(web_result)                    
        
        return web_results
    
    def _parse_news_results(self, response):
        """Go through and parse all the news results from the JSON response"""
        news_results = []
        
        for result in response['results']:
            # We had a bunch more fields in the BingV2 wrapper but doubt anything used them
            puppy_to_bing_keys = {"title"           :   ["Title"],
                                  "link"            :   ["Url"],
                                  "summary"         :   ["Description"],
                                  "source"          :   ["Source"],
                                  "date"            :   ["Date"]}
            
            news_result = self._result_parser(result, puppy_to_bing_keys)        
            news_results.append(news_result)        
        
        return news_results
    
    def _parse_video_results(self, query, response):
        """Go through and parse all the video results from the JSON response"""
        video_results = []
        
        for result in response['results']:                
            puppy_to_bing_keys = {"title"           :   ["Title"],
                                  "link"            :   ["MediaUrl"],
                                  "runtime"         :   ["RunTime"],
                                  "displayLink"     :   ["DisplayUrl"],
                                  "thumbnail"       :   ["Thumbnail", "MediaUrl"],
                                  "thumbnailWidth"  :   ["Thumbnail", "Width"],
                                  "thumbnailHeight" :   ["Thumbnail", "Height"],
                                  "thumbnailSize"   :   ["Thumbnail", "FileSize"],
                                  "thumbnailType"   :   ["Thumbnail", "ContentType"]}
            
            video_result = self._result_parser(result, puppy_to_bing_keys) 
            
            # There is no such field so just adding the query and that it's an image result
            video_result['summary'] = "Video result from a query for %s" % query.search_terms
                   
            video_results.append(video_result)
            
        return video_results
    
    def _parse_related_results(self, query, response):
        """Go through and parse all the related search results from the JSON response"""
        related_results = []
        
        for result in response['results']:
                
            puppy_to_bing_keys = {"title"           :   ["Title"],
                                  "link"            :   ["BingUrl"]}
            
            related_result = self._result_parser(result, puppy_to_bing_keys) 
            
            # There is no such field so just adding the query and that it's an related result
            related_result['summary'] = "Search Suggestion of: %s based on a query for: %s" % (related_result['title'], query.search_terms)
                   
            related_results.append(related_result)
        
        return related_results
    
    def _parse_spelling_results(self, query, results):
        """Go through and parse all the spelling suggestion results from the JSON response"""
        spelling_results = []
        
        # Instead of writing another parser just use regular expressions, only useful value is the suggestion itself
        suggestions = re.findall(r'\<\w{1}:Value\s*\w{1}:type="\w*\.\w*">(.*)<\/\w{1}:Value>', results)
        
        for suggestion in suggestions:
            spelling_result = {"title"        :   "Spelling Suggestion for: %s" % query.search_terms,
                               "summary"      :   "Query: %s; Suggested correction: %s" % (query.search_terms, str(suggestion)),
                               "link"         :   "",
                               "suggestion"   :   str(suggestion)}
            
            spelling_results.append(spelling_result)
        
        return spelling_results