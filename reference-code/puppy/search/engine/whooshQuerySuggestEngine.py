# -*- coding: utf8 -*-

from whoosh.index import open_dir, EmptyIndexError, IndexVersionError
from whoosh.index import IndexError as WhooshIndexError
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh import highlight

from puppy.search import SearchEngine
from puppy.model import Query, Response
from puppy.search.exceptions import SearchEngineError

class WhooshQuerySuggestEngine(SearchEngine):
    """
    Whoosh Query log search engine.

    Paramters:

    * resultsPerPage (int): select how many results per page

    * whoosh_query_index_dir (str): the absolute path for where you want queries indexed at
    """
  
    def __init__(self, service, whoosh_query_index_dir = "", resultsPerPage = 8, **args):
        super(WhooshQuerySuggestEngine, self).__init__(service, **args)
        self.resultsPerPage = resultsPerPage

        print "In construction of Whoosh Query log search engine"   
        try:
            self.queryIndex = open_dir( whoosh_query_index_dir )
            print "Whoosh query index open"
            print  self.queryIndex.doc_count()
        except EmptyIndexError, e: 		# Our Whoosh Index is empty
          print "The defined Whoosh query index is empty: " + whoosh_query_index_dir
          raise e
        except IndexVersionError, e: 	# Our Whoosh Index does not match our version of Whoosh
          print "There is a problem between the your version of Whoosh and the one in the query index at: " + whoosh_query_index_dir
          raise e
        except WhooshIndexError, e:		# Generic Index error if the above don't cover the index error
          print "There was a problem opening the Whoosh query index at: " + whoosh_query_index_dir
          raise e
        except Exception, e:			# Catch all exception just in case, the ones above should handle it though
          print "Could not open Whoosh query index at: " + whoosh_query_index_dir
          raise e  
  
    def search(self, query, pos=0):
        """
        Search service for query log data held in a Whoosh query index
        with a Schema(title=ID(unique=True, stored=True), content=TEXT(stored=True), ncontent=NGRAM(stored=True), issued=DATETIME(stored=True))
    
        Parameters:
  
        * query (puppy.model.Query)
  
        Returns:
  
        * results puppy.model.Response
  
        Raises:
  
        * ?  
        """
        def parse_whoosh_trec(site, query, results):
            response = Response()
            response.version = 'trec'
            response.feed.setdefault('title', "{0}: {1}".format(site, query))
            response.feed.setdefault('link','')
            response.feed.setdefault('description',"Search results for '{0}' at {1}".format(query, site))
            response.namespaces.setdefault("opensearch", "http://a9.com/-/spec/opensearch/1.1/")
            response.feed.setdefault("opensearch_totalresults", len(results) )
            response.feed.setdefault("opensearch_itemsperpage", len(results))
            response.feed.setdefault("opensearch_startindex", 1)
            response.feed.setdefault('query', query)
            
            try:
		duplicates=set()
		buff=""
                if len(results)>1:
                    resultNum = 1
                    for hit in results:
                        if resultNum > self.resultsPerPage:
                            break
                        
                        desc = hit.highlights("content")   
                        desc = desc.split("\t")[0]
                        
                        if desc not in duplicates and query.lower() != desc.lower() and desc !=(buff+"?"):
                            response.entries.append({'title': desc, 'link': '', 'summary': desc })
                            resultNum += 1
                            duplicates.add(desc)
			buff =desc
                else:
                        print "No hits found for query: " + query
            except Exception, e:
                print "Converting results to OpenSearch Failed"
            return response
            # end parse_whoosh_trec
          
        try:
            parser = QueryParser("content", self.queryIndex.schema)
            print query.search_terms
            myquery = parser.parse( query.search_terms  )
            results = []
            reponse = []
            rr={}
            with self.queryIndex.searcher() as searcher:
                results = searcher.search( myquery )
                
                
                for result in results:
		  temp = result['content']
		  temp = temp.split("\t")
		  sugg= temp[0]
		  print result
		  rr['content']= sugg
                results.fragmenter = highlight.ContextFragmenter(surround=40)
                results.formatter = highlight.UppercaseFormatter()
                
                response = parse_whoosh_trec('WhooshQueryEngine', query.search_terms, results)
            return response

        # -----  The Following are Whoosh errors -----

        # There's a problem with the Whoosh query created from the users query
        except QueryError, e:
          raise SearchEngineError("Whoosh Query Suggest Engine", e, errorType="Whoosh", query=query)

        # Our Whoosh Index is empty
        except EmptyIndexError, e: 		
          raise SearchEngineError("Whoosh Query Suggest Engine", e, errorType="Whoosh")

        # Our Whoosh Index does not match our version of Whoosh
        except IndexVersionError, e:
          raise SearchEngineError("Whoosh Query Suggest Engine", e, errorType="Whoosh")

        # Generic Index error if the above don't cover the index error
        except WhooshIndexError, e:		
          raise SearchEngineError("Whoosh Query Suggest Engine", e, errorType="Whoosh")

        # ----- The Following are standard Python errors -----

        # Check for a type error for resultsPerPage and when processing results
        except TypeError, e:
          if isinstance(self.resultsPerPage, int) == False:
            note = "Please ensure that 'resultsPerPage' is an integer."
            raise SearchEngineError("Whoosh Query Suggest Engine", e, note = note, resultsPerPageType = type(self.resultsPerPage))

          raise SearchEngineError("Whoosh Query Suggest Engine", e)

        # Catch Attribute error which deals with unexpected none type for the objects the wrapper uses and other associated issues
        except AttributeError, e:
          raise SearchEngineError("Whoosh Query Suggest Engine", e)