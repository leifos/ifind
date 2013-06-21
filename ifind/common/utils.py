__author__ = 'leif'

from selenium import webdriver
import Image

def take_screen_shot(url, path, name, height, width):
    """ given the url, take a screen shot and save it to the path/name with dimensions (height, width)

    Args:
        url: string to url of web page
        path: string of where to save the image
        height: integer (size of screen shot)
        width: integer

    Returns:
        None
    """
    driver = webdriver.PhantomJS()
    driver.set_window_size(width,height)
    driver.get(url)
    driver.save_screenshot(path + name)
    driver.quit()


def crop_screen_shot(source, destination, x1, y1, x2, y2):
    """ open source image, crop it with coords upper,left bottom,right

    Args:
        source: path of image
        destination: path of cropped image to be stored
        x1,y1: point in upper left corner of the crop rectangle
        x2,y2: point in the lower right corner of the crop rectangle

    Returns:
        None
    """
    im = Image.open(source)
    box = (x1,y1,x2,y2)
    region = im.crop(box)
    region.save(destination)

def halve_screen_shot(source,destination):
    """ open source image, save a cropped top half to destination
    """
    im = Image.open(source)
    [x,y] = im.size
    box = (0,0,x,y/2)
    region = im.crop(box)
    region.save(destination)

def get_page_title(driver):
    """ return web page title
    Args:
        driver: initialised webdriver with widow size set and web page retrieved
    """
    return driver.title()


def perform_query(query_terms):
    """ issue the query terms to bing
    Args:
        query_terms: string contain the query

    Returns:
        result: list of titles and urls in rank order

    """

    pass




