"""
Take a url, generate queries and calculate retreivability scores for the page.
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   08/08/2013
Version: 0.1

requires nltk: pip install nltk
"""

from SingleTermQueryGeneration import SingleTermQueryGeneration
from BiTermQueryGeneration import BiTermQueryGeneration
from QueryGeneration import QueryGeneration
from ifind.search.query import Query
from nltk import clean_html
from urllib import urlopen
import string


class PageRetrievabilityCalculator:
    """
    Given a url calculate the retrievability scores for that page.
    """

    def __init__(self, engine, cutoff):
        self.engine = engine
        self.cutoffRank= cutoff


    def calculate_retrievability(self, allScores):
        """
        calculates overall retrievability by summing scores contained
        in dictionary allScores
        :param allScores: a dictionary of query term and retrievability score pairs
        :return:the final retrievability of the document with the current search
        engine over all generated queries
        """
        #get the values, the query terms aren't needed
        allVals=allScores.values()
        #iterate through, sum and return
        finalResult = 0
        for val in allVals:
            finalResult += val
        return finalResult

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

        #instantiate the correct generator type dependent on isSingle
        if isSingle:
            generator = SingleTermQueryGeneration()
        else:
            generator = BiTermQueryGeneration()

        #use the generator to create the queries for the text, store
        #the result in a list

        queries = {}
        if isHtml:
            #copy url for use in calculateIndividualScore
            self.url = text
            content_source=self._getPage(text)#replace content source with actual source code
            queries = generator.extractQueriesFromHtml(content_source)
        else:
            queries = generator.extractQueriesFromText(text)
        print queries

        #create list of query objects so queries can be issued
        #against engines
        queryObjsList = []
        for query in queries:
            currQuery = Query(query, self.cutoffRank)
            queryObjsList.append(currQuery)
        #return the queries object list
        return queryObjsList

    def calculateIndividualScoreCumulative(self, query):
        #issue the query and store the results object
        results = self._issueQuery(query)
        #determine if query is in the list of results
        containsQuery = False
        for result in results:
            print result
            if result.url == self.url:
                containsQuery = True
                print "results contain " + self.url
                break
        if containsQuery:
            #the query has returned the document represented by url
            #within cutoff results, so f(k_dq,c) =1
            return 1
        else:
            return 0




    def _issueQuery(self,query):
        """
        Issues single query to the search engine and returns results
        object
        """
        print "issuing query : " + query.terms
        return self.engine._search(query)

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

        print  " %d queries generated, issuing queries to engine %s " %  (queryList.__len__() , self.engine.name)
        #can now issue the queries to the engine and get individual retreivability
        scores = {};
        queryNum = 0
        for query in queryList:
            print " query number : %d" % (queryNum)
            queryNum += 1
            currQueryRetreivability=self.calculateIndividualScoreCumulative(query)
            #add the value to a dictionary with key being query terms
            scores[query.terms]=currQueryRetreivability
        #now have a dictionary of individual retrievability scores
        #sum all results and print
        result = self.calculate_retrievability(scores)
        print result


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
        #make sure only single white spaces remain
        content = ' '.join(content.split())

        print content

        return content