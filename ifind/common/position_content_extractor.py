#!/usr/bin/env python
# -*- coding: latin-1 -*-

__author__ = 'rose'

from BeautifulSoup import BeautifulSoup
import re

class PositionContentExtractor(object):

    def __init__(self, div_ids=None):
        self.div_ids = div_ids
        self.html = ''
        self.html_soup = None
        self.text = ''

    def set_div_ids(self, ids):
        #print "here!"
        self.div_ids = ids
        #print ids
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
            else:
                return self.text

    def _remove_div_content(self):
        """
            returns a string with the content the html with the content of
            divs in div_ids removed
            :param div_ids: a list of the ids of the div to be removed
            :return:None
            """
        result = ''
        #for all div ids find the elements in the beautiful soup tree and extract
        #the corresponding div
        #this updates self.html_soup, if divs are reset then soup is regenerated

        for div_id in self.div_ids:
            #print "removing id ", div_id
            elem = self.html_soup.find("div", {"id": div_id})
            if elem:
                elem.extract()
        #set the text of the class to be the result of removing the text from the divs
        #use find all text, returns list, join list elements
        texts = self.html_soup.findAll(text=True)

        visible_elements = [self._visible_text(elem) for elem in texts]
        #visible_text = ''.join(visible_elements)
        visible_text = visible_elements

        cleaned = self._clean_result(visible_text)
        #print cleaned
        return cleaned


    def _clean_result(self, text):
        text = ' '.join(text)
        text = re.sub(r'\s+', ' ', text)
        #returns unicode, strip trailing and leading whitespace
        return text.strip()
        #return text

    def _calc_percentage(self, percentage, total_words):
        if total_words == 0:
            return 0
        else:
            return 100 * float(percentage)/float(total_words)



    def _visible_text(self, element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
            return ''
        result = re.sub('<!--.*-->|\r|\n', '', str(element), flags=re.DOTALL)
        result = re.sub('\s{2,}|&nbsp;', ' ', result)
        return result