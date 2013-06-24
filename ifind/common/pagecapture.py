from ifind.common import utils



class PageCapture:

    def __init__(self,url=None,width=800,height=600):
        self.driver = utils.webdriver.PhantomJS()
        self.driver.set_window_size(width,height)
        if url is not None:
            self.load_url(url)
        else:
            self.url = url

    def load_url(self,url):
        """ url format: 'http://www.example.com'

        args: take a url string
        returns: true if the page is loaded in the driver, else false

        """

        #check to make sure the url is loaded.
        self.driver.get(url)
        # if driver is loaded
        self.url = url
        return True
        # else:
        # self.url = None
        # return False

    def take_screen_shot(self, url, filename , height, width):
        if self.url:
            #self.driver
            utils.take_screen_shot(url, '', name, height, width)

    def crop_screen_shot(self, filename, x1, y1, x2, y2):
        utils.crop_screen_shot(destination, x1, y1, x2, y2)

    def halve_screen_shot(self, filename):
        """ args: filename - where the screen shot will be saved to.
        """
        utils.halve_screen_shot(source, destination)

    def get_page_title(self):
        return self.driver.title

    def get_page_sourcecode(self):
        return self.driver.page_source

