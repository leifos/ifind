__author__ = 'rose'
"""
This contains the code for more intelligent query extraction
based on the structure of the html
it will include parsing for specific divs
ignoring div id/classes
weighting based on importance of tags
"""
from xml.etree import ElementTree
from copy import deepcopy
from selenium import webdriver
import requests
from query_generation import BiTermQueryGeneration

class StructuredExtractor():
    """
    constructor takes a string of html and a
    """
    def __init__(self, html):
        self.html=html
        self.xml_tree = ElementTree.fromstring(self.html)


    def remove_div_content(self, div_ids):
        """
        returns a string with the content the html with the content of
        divs in div_ids removed
        :param div_ids: a list of the ids of the div to be removed
        :return: a string with the divs content removed
        """
        result = ''
        tree_copy = deepcopy(self.xml_tree)
        for div_id in div_ids:
            #need to check the children of the root and then their children
            for element in tree_copy:
                #if the child is a div with the target div id then use the parent to
                #remove the child
                if element.tag == 'div' and element.attrib['id'] == div_id:
                    tree_copy.remove(element)
                for child in element:
                    if child.tag == 'div' and child.attrib['id'] == div_id:
                        element.remove(child)
            #now traverse the copy with the div removed and store the results
        for node in tree_copy:
            if node.text:
                result += node.text
                #print "text of node is ", node.text
            for child in node:
                if child.text:
                    #print "text of node is ", child.text
                    result += child.text

        return result

    def get_node_content(self, node_tag):
        """
        pass the tag of text you want in, the text is returned
        None is returned if that node has no text, it
        doesn't look to children till it gets to text
        :param node_tag:
        :return:
        """
        content =''
        #for node in self.xml_tree.iter():
        #    print node.tag, node.attrib, node.text
        for node in self.xml_tree.iter(node_tag):
            if node.text:
                content = content + node.text
            return content

    def get_div_content(self, div_id):
        """
        returns the content of a div with a particular id
        :param div_id:
        :return:
        """
        #get a list of all div Elements
        all_divs= self.xml_tree.iter("div")
        #create a dom object from the string

        for div in all_divs:
            if div.attrib["id"] == div_id:
                #then we have the right div, go through all it's
                #children and gather their content
                content = ''
                for child in div:
                    if child.text:
                        content += child.text
                return content
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
        #iterate through the elements, when you find text get the
        #tag of the element and store it in a dictionary with the
        #key=tag value=text content
        #todo there will be duplicate tags which
        # will result in overriding content
        #  what do you want to do about this? append and group?
        related_text = {}
        #iterate through the elements in the tree adding to
        #dict when tag with content found which is not empty string
        for element in self.xml_tree.iter():
            if element.text != ' ':
                related_text[element.tag] = element.text
        return related_text

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
        pass

    def get_query_position(self, query, url):
        """
        takes a query and returns the first
        x,y location of the query in the page
        :param query:
        :return:
        """
        #driver = webdriver.PhantomJS()


        #selenium doesn't seem to have anything to find text
        #so could find the tag the query text first occurs in
        #then find the location by the tag
        target_tag = ''
        # for element in self.xml_tree.iter():
        #     if query in element.text.lower() :
        #         target_tag = element.tag
        #
        # el = driver.find_element_by_tag_name(target_tag)
        pass

    def create_biterm_queries(self):
        """
        goes through the related_text dictionary and creates a
        query list using bitermquerygen object for each tag
        combines into one query list and returns said list
        :return:
        """
        related_text_dic=self.get_all_related_text()
        all_queries = []
        for tag, content in related_text_dic.iteritems():
            generator = BiTermQueryGeneration()
            queries = generator.extract_queries_from_text(content)
            all_queries.append(queries)









