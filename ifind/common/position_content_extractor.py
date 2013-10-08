#!/usr/bin/env python
# -*- coding: latin-1 -*-

__author__ = 'rose'

from BeautifulSoup import BeautifulSoup
from copy import deepcopy

class PositionContentExtractor(object):

    def __init__(self, div_ids=None):
        self.div_ids = div_ids
        self.html = ''
        self.html_soup = None
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
        self.html_soup = BeautifulSoup(html)
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
        for div_id in self.div_ids:
            self.html_soup.find("div", {"id": div_id})
        return result



    def _calc_percentage(self, percentage, total_words):
        if total_words == 0:
            return 0
        else:
            return 100 * float(percentage)/float(total_words)



