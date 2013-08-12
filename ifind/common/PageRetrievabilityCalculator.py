"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1

requires nltk: pip install nltk
"""

from pagecapture import  PageCapture
from SingleTermQueryGeneration import SingleTermQueryGeneration
from BiTermQueryGeneration import BiTermQueryGeneration
from QueryGeneration import QueryGeneration
from ifind.search.query import Query
from nltk import clean_html
from urllib import urlopen

class PageRetrievabilityCalculator:
    """
    Given a url calculate the retrievability scores for that page.
    """

    def __init__(self, engine):
        self.engine = engine


    def calculate_retrievability(self):
        pass



    def _generateQueries(self, isHtml, isSingle, text):
        """
        generates a list of single or bi term queries from plain text or html
        returns said list
        :param isHtml boolean to denote if the text is html or not
        :param boolean isSingle to denote whether to generate single or bi-terms
        :param text the html or text from which queries will be generated
        :return returns a list of queries as strings
        """
        #setup a generic generator object
        generator = QueryGeneration()

        #a placeholder for the number of results returned
        top = 10
        #instantiate the correct generator type dependent on isSingle
        if(isSingle):
            generator = SingleTermQueryGeneration()
        else:
            generator = BiTermQueryGeneration()

        #use the generator to create the queries for the text, store
        #the result in a list
        queries = {}
        if(isHtml):
            content_source=self._getPage(text)#replace content source with actual source code
            queries = generator.extractQueriesFromHtml(content_source)
        else:
            queries = generator.extractQueriesFromText(text)

        #create list of query objects so queries can be issued
        #against engines
        queryObjsList = []
        for query in queries:
            currQuery = Query(query,top)
            #print currQuery.terms
            queryObjsList.append(currQuery)
        #return the queries object list
        return queryObjsList



    def _issueQueries(self,queryObjectList):
        """
        Issues query list to the search engine
        """
        for query in queryObjectList:
            result = self.engine._search(query)
            print result

    def _calculateScores(self, content_source,isHtml, isSingle):
        """
        calls getPage
        uses html to generateQueries
        issues the queries
        calculates the scores for the page and returns them
        may start as dictionary or list, but will probably extract an object
        which will be able to
        - rank queries by query_ret_score, and show top n queries
	    - rank queries by query_ret_score * query_prob, and show the top n queries
	    - show the number of queries issued, and the number of queries that were successful, and the page retrievability

        :return: dictionary or list of results

        Generates the queries for the page, issues them to the search engine, calculates
        the scores and returns a dictionary of results
        :param content_source either a url or the text from which queries are to be generated
        :param isHtml boolean indicating if the source is html or text
        :param isSingle boolean indicating if single terms are used, if false then biterms
        """

        print "generating queries from content "
        #can now generate the queries
        queryList = self._generateQueries(isHtml,isSingle,content_source)
        #for query in queryList:
        #    print query.terms

        #can now issue the queries to the engine - todo
        self._issueQueries(queryList)



    def _getPage(self, url):
        """
        Creates a PageCapture object, uses it to get_page_sourcecode
        :param url: the url of the page to be accessed
        :return: the content of the website for the given url less the html
        """

        #uses nltk.clean_html to extract only text content from the html
        #use urllib to open and read the html from the given url
        html = urlopen(url).read()
        content = clean_html(html)

        return content