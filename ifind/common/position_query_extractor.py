__author__ = 'rose'

class PositionQueryExtractor():
from xml.etree import ElementTree
from copy import deepcopy
from query_generation import BiTermQueryGeneration

    def __init__(self, html):
        self.html = html
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

    def get_subtext(self, text, num_words):
        """
        takes first num_words from text and return them as a string
        :param text:
        :return:
        """
        words = text.split()
        subtext = ''
        if len(words) > num_words:
            return subtext.join(words[0:num_words])
        else:
            return subtext.join(words)


    def generate_queries(self, text):
        """
        generates queries from the text passed in
        :return:
        """
        bi_gen= BiTermQueryGeneration()
        cleaned_term_list = bi_gen.clean_text(text)
        text = ''.join(cleaned_term_list)
        query_list = bi_gen.extract_queries_from_text(text)