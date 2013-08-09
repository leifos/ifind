"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1
"""

from pagecapture import  PageCapture
from SingleTermQueryGeneration import SingleTermQueryGeneration
from BiTermQueryGeneration import BiTermQueryGeneration
from QueryGeneration import QueryGeneration


class PageRetrievabilityCalculator:
    """
    Given a url calculate the retrievability scores for that page.
    """

    def __init__(self, engine):
        self.engine = engine


    def calculate_retrievability(self, content_source, isHtml, isSingle):
        """
        Generates the queries for the page, issues them to the search engine, calculates
        the scores and returns a dictionary of results
        :param content_source either a url or the text from which queries are to be generated
        :param isHtml boolean indicating if the source is html or text
        :param isSingle boolean indicating if single terms are used, if false then biterms
        """
        if(isHtml):#if it's html then use getPage to get the source of the url
            content_source=self._getPage(content_source)#replace content source with actual source code

        #can now generate the queries
        queryList = self._generateQueries(isHtml,isSingle,content_source)

        #can now issue the queries to the engine - todo


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

        #instantiate the correct generator type dependent on isSingle
        if(isSingle):
            generator = SingleTermQueryGeneration()
        else:
            generator = BiTermQueryGeneration()

        #use the generator to create the queries for the text, store
        #the result in a list
        queries = []
        if(isHtml):
            queries = generator.extractQueriesFromHtml(text)
        else:
            queries = generator.extractQueriesFromText(text)

        #return the queries list
        return queries



    def _issueQueries(self):
        """
        Issues query list to the search engine
        """
        pass

    def _calculateScores(self, url):
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
        """
        pass

    def _getPage(self, url):
        """
        Creates a PageCapture object, uses it to get_page_sourcecode
        :param url: the url of the page to be accessed
        :return: the source code of the website for the given url
        """
        #set a default height and width needed by constructor of PageCapture
        defaultWidth=800
        defaultHeight=600
        #create capture object
        capture= PageCapture(url,defaultWidth,defaultHeight)
        #get page sourcecode
        #need to add in some error handling
        content = capture.get_page_sourcecode()
        return content