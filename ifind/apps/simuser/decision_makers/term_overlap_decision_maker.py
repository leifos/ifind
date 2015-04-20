from loggers import Actions
from lxml.html.clean import Cleaner
from decision_makers import kl_divergence
from decision_makers.base_decision_maker import BaseDecisionMaker

class TermOverlapDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Uses term overlap counts from previously seen snippets and the current snippet to determine when to stop.
    """
    def __init__(self, search_context, stopword_file, threshold, query_based=True):
        super(TermOverlapDecisionMaker, self).__init__(search_context)
        
        self.__stopwords = self.__get_stopwords_list(stopword_file)
        self.__threshold = threshold
        self.__query_based = query_based  # Determines if the decision maker is query-based (i.e. only snippets/documents in a SERP) or session-based (i.e. all snippets/documents observed through a search session).
        
    def decide(self):
        """
        Determines whether the user should proceed to examine the subsequent snippet, or stop and issue a new query.
        """
        seen_text = ""
        existing = []
        
        if self.__query_based:  # If this is query-based, we look at only snippets that were examined in the current query.
            existing = self._search_context.get_examined_snippets()
        else:
            existing = self._search_context.get_all_examined_snippets()
        
        print existing
        
        
        return Actions.SNIPPET

    
    def __clean_markup(self, string_repr):
        """
        Given a string representation of a document or snippet, removes all HTML markup and returns it, cleaned.
        """
        if string_repr == "":
            return string_repr
        
        cleaner = Cleaner(allow_tags=[''], remove_unknown_tags=False)
        cleaned_text = cleaner.clean_html(string_repr)
        
        return cleaned_text[5:][:-6]  # Removes the extra <div>...</div> that is added
    
    def __get_stopwords_list(self, stopwords_filename):
        """
        Given the stopwords instance variable, returns a list of stopwords to use.
        Assumes that each word to be used is on a new line.
        """
        stopwords_file = open(stopwords_filename, 'r')
        stopwords = []
        
        for line in stopwords_file:
            line = line.strip()
            stopwords.append(line)
        
        stopwords_file.close()
        return stopwords