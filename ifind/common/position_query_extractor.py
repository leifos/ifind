__author__ = 'rose'

from xml.etree import ElementTree
from copy import deepcopy
from query_generation import BiTermQueryGeneration
from language_model import LanguageModel


class PositionQueryExtractor(object):

    def __init__(self, html, div_ids):
        self.html = html
        self.xml_tree = ElementTree.fromstring(self.html)
        self.div_ids=div_ids

    def set_div_ids(self, ids):
        self.div_ids = ids

    def remove_div_content(self):
        """
            returns a string with the content the html with the content of
            divs in div_ids removed
            :param div_ids: a list of the ids of the div to be removed
            :return: a string with the divs content removed
            """
        result = ''
        tree_copy = deepcopy(self.xml_tree)
        for div_id in self.div_ids:
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


    def get_subtext(self, text, num_words=0, percentage=None):
        """
            takes first num_words from text and return them as a string
            :param text:
            :return:
            """
        words = text.split()
        subtext = ' '
        if(percentage):
            num_words = round(self.calc_percentage(percentage,len(words)))
        if(num_words):
            if len(words) > num_words:
                return subtext.join(words[0:num_words])
                # for term in :
                #     print term
                #     subtext += ' '.join(term)
            else:
                return text


    def calc_percentage(self, percentage, total_words):
        if total_words == 0:
            return 0
        else:
            return 100 * float(percentage)/float(total_words)


    def generate_queries(self, text):
        """
            cleans and generates queries from the text passed in
            :return: list of text queries
            """
        #print "text is ", text
        bi_gen = BiTermQueryGeneration()
        query_list = bi_gen.extract_queries_from_text(text)

        #todo not sure if this will be needed
        #create dictionary of term, occurrence for use in language model
        # terms = {}
        # for term in query_list:
        #     if term in terms:
        #         terms[term] += 1
        #     else:
        #         terms[term] = 1
        # docLM = LanguageModel(term_dict=terms)
        ####

        return query_list

