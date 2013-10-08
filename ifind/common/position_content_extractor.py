#!/usr/bin/env python
# -*- coding: latin-1 -*-

__author__ = 'rose'

from xml.etree import ElementTree
from copy import deepcopy



class PositionContentExtractor(object):

    def __init__(self, div_ids=None):
        self.div_ids = div_ids
        self.html = ''
        self.xml_tree = None
        self.text = ''

    def set_div_ids(self, ids):
        self.div_ids = ids
        self.process_html_page(self.html)


    def process_html_page(self, html):
        """ reads in the html, parses it, and removes the set of specified div ids, assigning the text to self.text
        :param html: expects a valid html document
        :return: None
        """
        self.html = html
        self.xml_tree = ElementTree.fromstring(self.html)
        self.text = self._remove_div_content()

    def get_subtext(self, num_words=0, percentage=None):
        """
            takes first num_words from text and return them as a string
            :param text:
            :return:
            """
        words = self.text.split()
        subtext = ' '
        if(percentage):
            num_words = round(self._calc_percentage(percentage,len(words)))
        if(num_words):
            if num_words == 0:#return all text if 0 assumes 0 means wants all
                return self.text
            if len(words) > num_words:
                return subtext.join(words[0:num_words])
                # for term in :
                #     print term
                #     subtext += ' '.join(term)
            else:
                return self.text


    def _remove_div_content(self):
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



    def _calc_percentage(self, percentage, total_words):
        if total_words == 0:
            return 0
        else:
            return 100 * float(percentage)/float(total_words)



