# -*- coding: utf8 -*-

import urllib2
import _mssql  #support for sql server in python

from puppy.search import SearchEngine
from puppy.model import Query, Response

from puppy.search.exceptions import SearchEngineError

class EmmaSearchMSSQL(SearchEngine):
  """
  EmmaSearch search engine.

  Parameters:

  * age (str): values - 'v' for adults (shows all 'a' and 'k' results too), 'a' for teenagers, and 'k' for children

  * resultsPerPage (int): How many results per page - the default for the emma search service is 10
  """
  
  
  def __init__(self, service, age = 'v', resultsPerPage = 10, **args):
    super(EmmaSearchMSSQL, self).__init__(service, **args)
    self.age = age
    self.resultsPerPage = resultsPerPage
    
    #we define sql server database connection parameters
    
    #TODO replace these strings by system setting parameters
    
    self._server="utwks10760.ewi.utwente.nl\\SQLEXPRESS"
    self._user="puppy"
    self._password="puppyir"
    self._database="EmmaLibrary"
    self._database_bookstable="EmmaLibrary.dbo.emmakinderboeken"
    self._database_bookstable_id="EmmaLibrary.dbo.emmakinderboeken.Id"
    self._database_images = "EmmaLibrary.dbo.emmaboekenafbeenldigen"
    self._database_images_id="item_id"
    self._PATHFINDER_PATH="http://pathfinder.cs.utwente.nl/cgi-bin/opensearch/ekz.cgi?item="
    
    
    

  def _origin(self):
    """ This overrides SearchEngine's default origin (for results from a search engine) for Emma search """
    return 1

  # Go through and add link to pathfinder system (TODO Do we really need to show a link for this kind of search results?)
  def parseEmmaLinks(self, results):
    
    for result in results.entries:
        result['link']= self._PATHFINDER_PATH + str(result['id']).strip()
        
    return results

  # Go through each result and assign based on the puppy_age parameter and numeric age classification to the results
  def parseEmmaAge(self, results):	 
    for result in results.entries:
        if result.has_key('puppy_age'):
            if result['puppy_age'] == 'v':
                result['minAge'] = 20
                result['maxAge'] = 100
            elif result['puppy_age'] == 'a':
                result['minAge'] = 13
                result['maxAge'] = 19
            elif result['puppy_age'] == 'k':
                result['minAge'] = 0
                result['maxAge'] = 12
    return results
    
  def cleanXmlEmma(self,xml_text):
    # xml_text= xml_text.replace("_x0020_", " ") 
    xml_text= xml_text.replace("<row>", "<item>")
    xml_text = xml_text.replace("</row>", "</item>")
 
    xml_text = xml_text.replace("<Auteurs>", "<authors>") 
    xml_text = xml_text.replace("</Auteurs>", "</authors>") 
 
    xml_text = xml_text.replace("<Titel>", "<title>")
    xml_text = xml_text.replace("</Titel>", "</title>")
  
    xml_text = xml_text.replace("<Annotatie>", "<summary>") 
    xml_text = xml_text.replace("</Annotatie>", "</summary>") 
 
    xml_text = xml_text.replace("<Leeftijdscategorie>", "<puppy_age>")
    xml_text = xml_text.replace("</Leeftijdscategorie>", "</puppy_age>")
    
    return xml_text
    
  def search(self, query, limit):
    """
    Search function for Hospial Data.
  
    Parameters:
  
    * query (puppy.model.Query)

    * limit (int): maximum number of results returned by the search
  
    Returns:
  
    * results puppy.model.Response
  
    Raises:
  
    * Exception 
  
    """
    try:
      conn = _mssql.connect(server=self._server, user=self._user, password=self._password, database=self._database)

#      conn.execute_query('SELECT TOP ' + str(limit)+ ' * FROM '+ _database_bookstable + ' INNER JOIN FREETEXTTABLE('+ _database_bookstable+',*, \''+ query+'\') as ft ON ft.[KEY]=' + _database_bookstable_id+ ' ORDER BY ft.RANK DESC FOR xml raw, ELEMENTS;')
  
      sql_query ='SELECT  temp.Id, temp.Titel, temp.Auteurs, temp.Leeftijdscategorie, temp.Annotatie, temp.ISBN, temp.Editie, temp.Uitgever, temp.[Classificatie code], temp.[Jaar van uitgave], temp.[Plaats van uitgave], temp.[Ref Type], temp.[Prijs], temp.[Serie], img.location  FROM (SELECT TOP ' + str(self.resultsPerPage)+ ' * FROM '+ str(self._database_bookstable) + ' INNER JOIN FREETEXTTABLE('+ self._database_bookstable+',*,\''+ query.search_terms+'\') as ft ON ft.[KEY]=Id ORDER BY ft.RANK DESC) as temp LEFT OUTER JOIN '+ str(self._database_images)+' as img ON temp.Id = img.item_id  FOR xml raw, ELEMENTS;';
    
  
      conn.execute_query(sql_query)
      response=""
   
      for row in conn:
	response = response + row[0].strip()

      response = self.cleanXmlEmma(response)
      #add rss tag for parsing
      response = "<rss>" + response + "</rss>"

      
      results = Response.parse_feed(response)

      results = self.parseEmmaAge(results)
      results = self.parseEmmaLinks(results)
      return results

     # Catch all exception, just in case
    except Exception, e:
      raise SearchEngineError("PuppyIR Emma Sql Server Search", e)
