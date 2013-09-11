__author__ = 'rose'
"""
To deal with cleaning the terms, this file contains a TermPipeline class
 as well as TermProcessors, a TermPipeline is made of processors and
 runs a term provided through each of the processors in the list to see
 if a cleaned term is returned at the end
"""

class TermPipeline():
    """

    """

    def __init__(self, term, minlength=3, stopfile=None):
        """
        constructor for TermPipeline
        :return:
        """
        #lower case
        term=term.lower()
        self.pipeline = []
        self.term = term
        self.min_length = minlength
        self.stoplist = []
        if stopfile:
            self.read_stopwordfile(stopfile)
        #create the term processors and add to the processor list
        self.set_processors()

    def set_processors(self):
        length_proc =LengthTermProcessor(self.term)
        length_proc.set_min_length(self.min_length)
        punct_proc = PunctuationTermProcessor(self.term)
        stop_proc= StopwordTermProcessor(self.term)
        stop_proc.set_stoplist(self.stoplist)
        alpha_proc = AlphaTermProcessor(self.term)

        self.pipeline.append(length_proc)
        self.pipeline.append(punct_proc)#punct processor needs to be before alpha proc otherwise returns None
        self.pipeline.append(stop_proc)
        self.pipeline.append(alpha_proc)

    def read_stopwordfile(self, stopwordfile):
        if stopwordfile:
            stopwords = open(stopwordfile).readlines()
            for term in stopwords:
                self.stoplist.append(term.strip())
        #print self.stoplist


    def perform_checks(self):
        """
        goes through each processor in the pipeline, stops if
        term is removed at any point
        :return:
        """
        for processor in self.pipeline:
            #for each processor in the pipeline perform the check
            #if returns None at any point, exit the pipeline
            #first set the processor term to be the current term
            processor.set_term(self.term)
            #now perform the check
            result = processor.check()
            #return None if no term left
            if result is None:
                return None
            #else set the term to be the result
            else:
                self.term = result
        #if the pipeline has gone through all checks, return term
        return self.term

class TermProcessor():
    """

    """

    def __init__(self, term):
        """

        :return:
        """
        self.set_term(term)

    def set_term(self, term):
        self.term = term


    def check(self):
        return None

class LengthTermProcessor(TermProcessor):

    def set_min_length(self, min_len):
        if(min_len>0):
            self.min_len = min_len
        else:
            self.min_len=1

    def check(self):
        """
        :param term: takes a term
        :return: returns the term, if it meets the minimum length criteria
        """
        if len(self.term) >= self.min_len:
            return self.term
        else:
            return None

class PunctuationTermProcessor(TermProcessor):

    def check(self):
        """remove punctation surrounding a term
        :param term:
        :return: term without punctation
        """
        #get the last character
        #is there a possibility multiple punctuation at start and end?
        length = len(self.term)
        firstChar = self.term[0:1]
        if str(firstChar).isalnum():
            self.term = self.term
        else:
            #print "cutting first letter " + firstChar + " from " +term
            self.term = self.term[1:length]
            #print "term now " +term
        #get length again incase punctuation at start and end
        length = len(self.term)
        lastChar = self.term[length-1:length]
        if str(lastChar).isalnum():
            self.term = self.term
        else:
            #print "cutting last letter " + lastChar + "from " + term
            self.term = self.term[0:length-1]
            #print " is now " + term

        #now check if there's nothing left, then don't add, if there is, add it
        if self.term:
            return self.term
        else:
            return None

class StopwordTermProcessor(TermProcessor):

    def set_stoplist(self, stoplist):
        self.stoplist=stoplist
        #print self.stoplist

    def check(self):
        if self.term in self.stoplist:
            return None
        else:
            return self.term

class AlphaTermProcessor(TermProcessor):

    def check(self):
        if self.term.isalpha():
            return self.term
        else:
            return None
