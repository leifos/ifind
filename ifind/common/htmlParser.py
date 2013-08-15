"""
A class which parses html and collects the content into a string of text
=============================
Author: rose : <Rosanne.English@glasgow.ac.uk>
Date:   09/08/2013
Version: 0.1
"""
from HTMLParser import HTMLParser
from re import sub


class htmlParser(HTMLParser):
    """
    takes some Html and puts the content into a string of text
    ignoring the tags
    """
    _text = ""
    #a boolean to track if we're in the head, in which case ignore the
    #content between tags as these are irrelevant for generating queries
    #initialised to be true as head is at start of doc
    # and we parse sequentially. set to false once end tag for head occurs
    _inHeadTag=True
    #to track if we're in a script tag, ignore contents if so
    _inScriptTag = False

    def __init__(self, html):
        """
        takes html, feeds it into the parser
        :param html:the html from which the content is to be extracted
        """
        HTMLParser.__init__(self)
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if(tag == "script"):
            self._inScriptTag =True

    def handle_endtag(self, tag):
         if(tag == "head"):
             #have now reached the end tag for head
             print "****REACHED THE END OF THE HEAD TAG****"
             self._inHeadTag=False
         if(tag == "script"):
             self._inScriptTag = False


    def handle_data(self, data):
        """
        concatenates the content between tags with the exception of the head
        :param data: the content between the current tag start and end
        """
        if(self._inHeadTag == False):
            text = data.strip()
            if len(text) > 0:
                text = sub('[ \t\r\n]+', ' ', text)

            self._text = self._text + " " + text

    def getText(self):
        """
        accessor method for the text
        :return: string of text extracted from the html
        """
        return self._text
