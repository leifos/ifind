# -*- coding: utf8 -*-

import urllib2
from lxml import etree

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError, ApiKeyError

class WebSpellChecker(SearchEngine):
  """
  Web Spell Checker's search engine api.

  You must include your application's Web Spell Checker Api key in your service manager config to use this service
  It should be under the identifier "web_spell_api_key"

  Parameters:

  * language (str): the language/dictionary to check again i.e. 'en_US' for American English, 'nl_NL' for Dutch etc (this is case sensative)

  """
    
  def __init__(self, service, language = 'en_GB', **args):
    super(WebSpellChecker, self).__init__(service, **args)
    self.language = language
   
  def search(self, query, offset):
    """
    Search function for Web Spell Search.        
    
    Parameters:
    
    * query (puppy.model.Query)
    
    Returns:
    
    * puppy.model.Response
    
    Raises:
    
    * urllib2.URLError
    
    """
    
    def parse_web_spell_checker_xml(site, url, query, results):
      """      
      Web Spell Checker's search API returns results in XML format. This function simply loads the XML into memory and creates an equivalent representation that is OpenSearch compliant.
      
      Parameters:
      
      * site (str): search engine name
      * url (str): the url for the results that were retrieved to use as the OpenSearch link for the response
      * query (str): query search terms (n.b. not a OpenSearch Query object)
      * results (dict): results from service
      
      Returns:
      
      * puppy.model.OpenSearch.Response
      
      """
      response = Response()
      response.version = 'xml'
      response.feed.setdefault('title', "{0}: {1}".format(site, query))
      response.feed.setdefault('link', url)
      response.feed.setdefault('description', "Search results for '{0}' at {1}".format(query, site))
      response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
      response.feed.setdefault("opensearch_itemsperpage", '')
      response.feed.setdefault("opensearch_startindex", 0)
      
      root = etree.XML(results)
      section = root.find("misspelling")
      suggestions = section.find("suggestions")

      for item in suggestions:
        try:
          suggestion = item.text
          spell_dict = {"title": "Spelling Suggestion for: '{0}'".format(query),  "link": ''}
          spell_dict['summary'] = "Original query: '{0}'. Suggested correction of query: '{1}'.".format(query, suggestion) 
          spell_dict['suggestion'] = suggestion
          response.entries.append(spell_dict)
        except Exception, e:
          print "Skipping a result due to: {0} \nWhen parsing a result from: {1}\n".format(e, url)
          continue              
      
      response.feed.setdefault("opensearch_totalresults", len(response.entries))
      return response

	# Try and get the API key from config, if it's not there raise an API Key error - the application will have to deal with this
    try:
      appId = self.service.config["web_spell_api_key"]
    except KeyError:
      raise ApiKeyError("Web Spell Checker", "web_spell_api_key")

    try:    
      url = "http://svc.webservius.com/v1/spellcheck/spellcheck/?wsvKey={0}&cmd=check_spelling&version=1.0&out_type=words&slang={1}&text={2}".format(appId, self.language, urllib2.quote(query.search_terms))
      data = urllib2.urlopen(url)
      return parse_web_spell_checker_xml('Web Spell Checker', url, query.search_terms, data.read())

    # urllib2 - this catches http errors due to the service being down, lack of a proxy etc
    except urllib2.URLError, e:
      raise SearchEngineError("Web Spell Checker", e, errorType = 'urllib2', url = url)
      
    # Catches any xml syntax errors that occur when lxml is parsing the results   
    except etree.XMLSyntaxError, e:
      raise SearchEngineError("Web Spell Checker", e, errorType = 'lxml', url = url)
      
    # Generic lxml error for errors other than syntax ones (future work might be to select more specific ones like above) 
    except etree.LxmlError, e:
      raise SearchEngineError("Web Spell Checker", e, errorType = 'lxml', url = url)
      
    # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
    except AttributeError, e:
      raise SearchEngineError("Web Spell Checker", e, url = url)