from ifind.common import utils



class PageCapture:

    def __init__(self,width,height):
        self.driver = utils.webdriver.PhantomJS()
        self.driver.set_window_size(width,height)

    def get_webpage(self,url):
        """ url format: 'http://www.example.com' """
        self.driver.get(url)

    def take_screen_shot(self, url, path, name, height, width):
        utils.take_screen_shot(url, path, name, height, width)

    def crop_screen_shot(self, source, destination, x1, y1, x2, y2):
        utils.crop_screen_shot(source, destination, x1, y1, x2, y2)

    def halve_screen_shot(self, source, destination):
        utils.halve_screen_shot(source, destination)

    def get_page_title(self):
        return self.driver.title

    def get_page_sourcecode(self):
        return self.driver.page_source


