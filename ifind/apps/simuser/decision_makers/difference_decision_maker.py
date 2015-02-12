from loggers import Actions
from lxml.html.clean import Cleaner
from decision_makers import kl_divergence
from decision_makers.base_decision_maker import BaseDecisionMaker

class DifferenceDecisionMaker(BaseDecisionMaker):
    """
    A concrete implementation of a decision maker.
    Using KL-Divergence to determine how "different" snippets/documents are to one another, makes a decision what to do next.
    """
    def __init__(self, search_context, stopwords_filename, threshold, nonrel_only=False, query_based=True):
        super(DifferenceDecisionMaker, self).__init__(search_context)
        
        self.__stopwords = self.__get_stopwords_list(stopwords_filename)
        self.__threshold = threshold
        self.__query_based = query_based  # Determines if the decision maker is query-based (i.e. only snippets/documents in a SERP) or session-based (i.e. all snippets/documents observed through a search session).
        self.__nonrel_only = nonrel_only
        
    def decide(self):
        """
        Determines whether the user should proceed to examine the subsequent snippet, or stop and issue a new query.
        """
        existing = self._search_context.get_all_examined_snippets()
        existing_str = ""
        
        if self.__query_based:  # If this is query-based, we look at only snippets that were examined in the current query.
            existing = self._search_context.get_examined_snippets()
        
        if len(existing) > 0:  # At least one snippet has been examined; we need to chop the last one off (as it is the current snippet).
            existing = existing[:-1]
            
            if self.__nonrel_only:  # Filter to only nonrelevant documents using a list comprehension.
                existing = [snippet for snippet in existing if snippet.judgment < 1]
        
        if len(existing) == 0:  # Nothing has been examined yet! So we just say proceed to the next snippet - nothing to compare against.
            return Actions.SNIPPET
        
        for snippet in existing:
            existing_str = "{0} {1} {2}".format(existing_str, snippet.title, self.__clean_markup(snippet.content))
        
        current_snippet = self._search_context.get_current_snippet()
        current_snippet_str = "{0} {1}".format(current_snippet.title, self.__clean_markup(current_snippet.content))
        
        if kl_divergence(current_snippet_str, existing_str) <= self.__threshold:
            return Actions.QUERY  # Too similar? Abandon the query and move to the next one.
        
        return Actions.SNIPPET  # Very different, so proceed to examine the next snippet.
    
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