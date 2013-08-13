"""
A class which parses html and collects the content into a string of text
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   09/08/2013
Version: 0.1
"""
from HTMLParser import HTMLParser

class htmlParser(HTMLParser):
    """
    takes some Html and puts the content into a string of text
    ignoring the tags
    """
    _text = ""
    def __init__(self, html):
        """
        takes html, feeds it into the parser
        :param html:the html from which the content is to be extracted
        """
        self.feed(html)


    def handle_data(self, data):
        """
        concatenates the content between tags
        :param data: the content between the current tag start and end
        """
        self._text = self._text + " " + data

    def getText(self):
        """
        accessor method for the text
        :return: string of text extracted from the html
        """
        return self._text
