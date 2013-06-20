__author__ = 'leif'

from selenium import webdriver

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



def perform_query(query_terms):
    """ issue the query terms to bing
    Args:
        query_terms: string contain the query

    Returns:
        result: list of titles and urls in rank order

    """

    pass




