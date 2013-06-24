"""
Take & crop screenshots of web pages, save them to disk
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   24/06/2013
Version: 0.1

Requires:
---------
      selenium, PIP, PhantomJS
"""

from selenium import webdriver
import Image


class PageCapture:
    """ Take & crop screenshots of web pages, save them to disk """

    def __init__(self,url=None,width=800,height=600):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(width,height)
        self.scrshot = None
        if url is not None:
            self.load_url(url)
        else:
            self.url = url

    def load_url(self,url):
        """ url format: 'http://www.example.com'

        args: take a url string
        returns: True if the page is loaded in the driver, else False

        """
        self.driver.get(url)
        page = self.driver.current_url
        # if driver is loaded
        if page != "about:blank":
            self.url = page
            return True
        else:
            self.url = None
            return False

    def take_screen_shot(self, filename):
        """ given the url, take a screen shot and save it to the path/name with dimensions (height, width)

        Args:
            url: string to url of web page
            path: string of where to save the image
            height: integer (size of screen shot)
            width: integer

            Returns:
                True if success, False otherwise
        """
        if self.url:
            success = self.driver.save_screenshot(filename)
            if success:
                self.scrshot = Image.open(filename)
                return True
            return False
        else:
            print ("Get an url first!")
            return False


    def crop_screen_shot(self, filename, x1, y1, x2, y2):
        """ open source image, crop it with coords upper,left bottom,right

        Args:
            source: path of image
            destination: path of cropped image to be stored
            x1,y1: point in upper left corner of the crop rectangle
            x2,y2: point in the lower right corner of the crop rectangle

        Returns:
            True if success, False otherwise
        """
        if self.scrshot is not None:
            box = (x1,y1,x2,y2)
            region = self.scrshot.crop(box)
            region.save(filename)
            return True
        else:
            print ("Take a screen shot first!")
            return False


    def halve_screen_shot(self, filename):
        """ args: filename - where the screen shot will be saved to.

            Returns:
                True if success, False otherwise
        """
        if self.scrshot is not None:
            [x,y] = self.scrshot.size
            box = (0,0,x,y/2)
            region = self.scrshot.crop(box)
            region.save(filename)
            return True
        else:
            print ("Take a screen shot first!")
            return False


    def get_page_title(self):
        """ Returns web page title """
        return self.driver.title


    def get_page_sourcecode(self):
        """Returns page source code """
        return self.driver.page_source

