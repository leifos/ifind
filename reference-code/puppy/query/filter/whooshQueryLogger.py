# -*- coding: utf8 -*-
import datetime
import string
from puppy.query import QueryFilter
from puppy.model import Query
from whoosh.index import exists_in, open_dir, create_in
from whoosh.fields import *

class WhooshQueryLogger(QueryFilter):
  """
  Logs the queries in a Whoosh Index, 
  Creates a Whoosh Index to store queries if there is no index in the dir given
  with a Schema(title=ID(unique=True, stored=True), content=TEXT(stored=True), ncontent=NGRAM(stored=True), issued=DATETIME(stored=True))
  Parameters:

  * order (int): filter precedence

  * whoosh_query_index_dir (string): path to the directory of the index

  * unique (boolean): indicates whether all queries are stored, or only unique queries (i.e. if unique=True)
  """
  
  def __init__(self, order=0, whoosh_query_index_dir="", unique=True):
   
    super(WhooshQueryLogger, self).__init__(order)
    self.description = "Adds queries to a Whoosh index"
    self.unique = unique
    print "About to create Whoosh query logger"
    self.whooshIndexDir = whoosh_query_index_dir
    schema = Schema(title=ID(unique=True, stored=True), content=TEXT(stored=True), ncontent=NGRAM(stored=True), issued=DATETIME(stored=True))
    if not exists_in(self.whooshIndexDir):
        print "Creating a Whoosh Index."
        create_in(self.whooshIndexDir, schema)
    self.queryIndex = open_dir(self.whooshIndexDir)
    print "The current number of queries held in the index is: " + str( self.queryIndex.doc_count() )
    print "Done creating Whoosh query log index"
  
  def filter(self, query):
    """Takes the query and adds it to a Whoosh index.
    
    Parameters:
    
    * query (puppy.model.Query): original query
    
    Returns:
    
    * query (puppy.model.Query): original query
    
    """

    print "About to write: " + query.search_terms + " to the Whoosh query log."
    if query.search_terms:
        writer = self.queryIndex.writer()
        if self.unique:
            try:
                writer.update_document(title=query.search_terms, content=query.search_terms, ncontent=query.search_terms, issued=datetime.datetime.now() )
            except:
                writer.add_document(title=query.search_terms, content=query.search_terms, ncontent=query.search_terms, issued=datetime.datetime.now() )
        else:
            writer.add_document(title=query.search_terms, content=query.search_terms, ncontent=query.search_terms, issued=datetime.datetime.now() )
        writer.commit()
    print "Whoosh query log contains: " + str(self.queryIndex.doc_count() )    

    return True
    #return query
