__author__ = 'leif'

import os, os.path
from puppy.service import ServiceManager, SearchService
from experiment_configuration import my_whoosh_doc_index_dir


# -*- coding: utf8 -*-
from puppy.search import SearchEngine
from puppy.model import Query, Response
from whoosh.index import open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import highlight

class WhooshTRECNewsEngine(SearchEngine):
    """Whoosh Query log search engine."""

    def __init__(self, service, whoosh_trec_news_index_dir=""):
        super(WhooshTRECNewsEngine, self).__init__(service)
        try:
            self.docIndex = open_dir( whoosh_trec_news_index_dir )
            print "Whoosh Document index open"
            print  self.docIndex.doc_count()
        except:
            print "Could not open Whoosh Document index at: " + whoosh_trec_news_index_dir

    def search(self, query, pos=0):
        """
        Search service for query log data held in a Whoosh TREC News Document index
        with a Schema()

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
            response.feed.setdefault("opensearch_totalresults", results.pagecount )
            response.feed.setdefault("opensearch_itemsperpage", pagelen)
            response.feed.setdefault("opensearch_startindex", results.pagenum)
            response.feed.setdefault('query', query)
            try:
                r = 0
                if len(results)>1:
                    for hit in results:
                        r = r + 1
                        title = hit["title"]
                        title = title.strip()
                        if len(title) < 1:
                            title = query
                        rank = ((int(results.pagenum)-1) * results.pagelen) + r
                        link = "/treconomics/" + str(hit.docnum) + "?rank="+str(rank)
                        desc = hit.highlights("content")
                        docid = hit["docid"]
                        docid = docid.strip()
                        source = hit["source"]
                        response.entries.append({'title': title, 'link': link, 'summary': desc, 'docid': docid ,'source': source})
                else:
                    print "No hits found for query: " + query
            except Exception, e:
                print "Converting results to OpenSearch Failed"
            return response
            # end parse_whoosh_trec

        try:
            parser = QueryParser("content", self.docIndex.schema)
            #mparser = MultifieldParser(["title", "content"], schema=self.docIndex.schema)
            print "In WhooshTRECNewsEngine: " + query.search_terms
            query_terms = parser.parse( query.search_terms  )

            page = query.start_page
            pagelen = query.page_len
            #print query_terms
            #print "page len" + str(pagelen)
            results = []
            reponse = []
            with self.docIndex.searcher() as searcher:
                results = searcher.search_page( query_terms, page, pagelen=pagelen )
  #             results = searcher.search( query_terms )

                results.fragmenter = highlight.ContextFragmenter(maxchars=300, surround=300)
                results.formatter = highlight.HtmlFormatter()
                results.fragmenter.charlimit = 100000

                print "WhooshTRECNewsEngine found: " + str(len(results)) + " results"
                print  "Page %d of %d - PageLength of %d" % (results.pagenum, results.pagecount, results.pagelen)
                response = parse_whoosh_trec('WhooshTRECNewsEngine', query.search_terms, results)
            return response
        except:
            print "Error in Search Service: Whoosh TREC News search failed"



config = { "log_dir": "treconomics/query_logs",  }

# create a ServiceManager
service = ServiceManager(config)

# create a SearchService, choose search engine and enable query logging
trec_search_service = SearchService(service, "trec_search")

trec_search_service.search_engine = WhooshTRECNewsEngine(trec_search_service, my_whoosh_doc_index_dir)
# add SearchService to ServiceManager
service.add_search_service(trec_search_service)