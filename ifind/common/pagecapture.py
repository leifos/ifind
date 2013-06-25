"""
Take & crop screenshots of web pages, save them to disk
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   24/06/2013
Version: 0.1

Requires:
---------
      selenium, PIL, PhantomJS
"""
from selenium import webdriver
import Image
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class PageCapture:
    """ Take & crop screenshots of web pages, save them to disk """


    def __init__(self,url=None,width=800,height=600):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(width,height)
        self.screen_shot = None

        self.url = url
        if url:
            self.load_url(url)

    def _check_url(self, url):
        """ Checks the validity of an url
            Returns True if valid, False otherwise
        """
        val = URLValidator()
        try:
            val(url)
        except ValidationError, e:
            print e
            return False
        return True

    def _ensure_screen_shot(self,filename):
        if not self.screen_shot:
            self.take_screen_shot(filename)

    def load_url(self,url):
        """ url format: 'http://www.example.com'

        args: take a url string
        returns: True if the page is loaded in the driver, else False

        """
        # check the url string. does it have http:// or not?
        if not self._check_url(url):
            return False

        self.driver.get(url)
        #set page_url to what the driver returns, a redirect might occur
        #upon request and url and driver.current_url might not be the same
        page_url = self.driver.current_url
        # if driver is loaded
        #if no url is loaded, driver.current_url = string "about:blank"
        if page_url != "about:blank":
            self.url = page_url
            return True
        else:
            self.url = None
            return False

    def take_screen_shot(self, filename):
        """ given the url, take a screen shot and save it to the
            path/name with dimensions (height, width)

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
                self.screen_shot = Image.open(filename)
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

        Returns: None
        """
        self._ensure_screen_shot(filename)
        box = (x1,y1,x2,y2)
        region = self.screen_shot.crop(box)
        #save region back into the instance var
        self.screen_shot = region
        region.save(filename)

    def resize_screen_shot(self, filename, height, width):
        """ resize a screen shot to size height,width and save it to
            filename. If screen shot not yet made, takes a screen
            shot first.

            Returns: None
        """
        self._ensure_screen_shot(filename)
        #resize() takes a tuple as an argument
        size = (height, width)
        resized = self.screen_shot.resize(size,Image.ANTIALIAS)
        resized.save(filename)

    def halve_screen_shot(self, filename):
        """ args: filename - where the screen shot will be saved to.

            Returns:
                True if success, False otherwise
        """
        if self.screen_shot:
            [x,y] = self.screen_shot.size
            box = (0,0,x,y/2)
            region = self.screen_shot.crop(box)
            region.save(filename)
            #save the cropped image back into instance var
            self.screen_shot = Image.open(filename)
            return True
        else:
            return False

    def get_page_title(self):
        """ Returns web page title """
        return self.driver.title

    def get_page_sourcecode(self):
        """Returns page source code """
        return self.driver.page_source

