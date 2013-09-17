__author__ = 'rose'
"""
This contains the code for more intelligent query extraction
based on the structure of the html
it will include parsing for specific divs
ignoring div id/classes
weighting based on importance of tags
"""
from xml.dom import minidom

class StructuredExtractor():
    """
    constructor takes a string of html and a
    """
    def __init__(self, html, ignore_divs=[]):
        self.html=html
        self.xml_tree = minidom.parseString(self.html)
        self.ignore_divs=ignore_divs

    def remove_ignored_content(self):
        """
        removes content from the list of ignored divs
        and returns the result
        :return: a string with the content contained in the ignored divs removed
        """
        pass

    def remove_div(self, div_id):
        """
        returns a string with the content of a div with div_id removed
        :param div_id: the id of the div to be removed
        :return: a string with the div removed
        """
        reduced_dom=self.xml_tree
        for div in self.xml_tree:
            if div.attributes["id"] == div_id:
                reduced_dom.removeChild()

    def get_div_content(self, div_id):
        """
        returns the content of a div with a particular id
        :param div_id:
        :return:
        """
        #get a string with all divs content
        div_contents = self.get_content("div")
        #create a dom object from the string
        div_dom= minidom.parseString(div_contents)
        for div in div_dom:
            if div.attributes["id"] == div_id:
                return div.toxml()
        #if you get this far then the id doesn't exist, return none
        return None

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


    def get_content(self, tag):
        """
        returns the content for a given tag
        :param tag: the tag for which the content is required
        :return: the content of a tag
        """
        content = self.xml_tree.getElementsByTagName(tag)
        result = ''
        if content:
            for part in content:
                result += part.toxml()
                print result
            return result
        else:
            return None




