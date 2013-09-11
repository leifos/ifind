__author__ = 'rose'
"""
This contains the code for more intelligent query extraction
based on the structure of the html
it will include parsing for specific divs
ignoring div id/classes
weighting based on importance of tags
"""
import nltk

class StructuredExtractor():
    """
    constructor takes a string of html
    """
    def __init__(self, html, ignore_divs=[]):
        self.html=html
        self.ignore_divs=ignore_divs

    def remove_ignored_content(self):
        """
        removes content from the list of ignored divs
        and returns the result
        :return:
        """
        pass

    def get_div_content(self, div_id):
        """
        returns the content of a div with a particular id
        :param div_id:
        :return:
        """

    def get_all_related_text(self):
        """
        goes through the html and returns a dictionary of strings
        which contain the content of each element, element name
        is the key content is the value
        could remove ignored divs content before creating the list
        :return:
        """
        pass

    def assign_tag_weightings(self):
        """
        not sure about this ---- present the tags in the page
        to the user using the console, ask each in turn
        what weighting, then return a list of weighted_text objects
        which have the element, the content, and the weighting
        maybe get_all_related text could return similar but without
        weightings assigned?
        :return:
        """

    def get_query_position(self, query):
        """
        takes a query and returns the first
        x,y location of the query in the page
        :param query:
        :return:
        """


