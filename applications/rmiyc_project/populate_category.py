import ifind.common.utils
import string
from ifind.common.pagecapture import PageCapture
from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from rmiyc.models import Page, Category
import os
from django.core.files import File
import httplib
from urlparse import urlparse


def convert_url_to_filename(url):

    '''
    :param url: Takes a url string
    :return: a valid filename constructed from the string

    >>> convert_url_to_filename("http://www.google.com")
    'www-google-com'
    >>> convert_url_to_filename("http://www.dcs.gla.ac.uk/~leif/index.html")
    'www-dcs-gla-ac-uk-leif-index-html'
    >>> convert_url_to_filename("www.ball.com/dj")
    'www-ball-com-dj'
    '''

    # Remove the http:// from the url as it is common among all the urls
    url = url.replace('http://', '')
    valid_chars = "-_.()/ %s%s" % (string.ascii_letters, string.digits)
    # Uses a whitelist approach: any characters not present in valid_chars are removed
    # spaces,slashes and dots are replaced with dashes
    filename = ''.join(c for c in url if c in valid_chars)
    filename = filename.replace(' ', '-')  # to replace spaces in file names with dashes.
    filename = filename.replace('/', '-')  # to replace slashes in file names with dashes.
    filename = filename.replace('.', '-')  # to remove dots in file names.
    return filename


def read_in_urls(filename):
    # read in file - store in a list (url_list)
    # Open the file with read only permit
    f = open(filename, 'r')
    # Read the first line
    print 'file is opened'
    url_list = []
    for line in f:
        # Strip urls from spaces
        url = line.strip()
        # is it a well-formed url string
        # Abdullah: url format rules are so flexible so it doesn't make sense (for me) to validate them
        # validate the url
        if checkUrl(url):
            url_list.append(url)

    f.close()
    print 'file is closed'
    return url_list


def checkUrl(url):
    '''
    :param url: takes a url string
    :return: true if the url exists on the web
            false: if the url does not exist on the web
    >>> urlparse('//www.cwi.nl:80/%7Eguido/Python.html')
    ParseResult(scheme='', netloc='www.cwi.nl:80', path='/%7Eguido/Python.html', params='', query='', fragment='')
    >>> urlparse('www.cwi.nl/%7Eguido/Python.html')
    ParseResult(scheme='', netloc='', path='www.cwi.nl:80/%7Eguido/Python.html', params='', query='', fragment='')
    >>> urlparse('help/Python.html')
    ParseResult(scheme='', netloc='', path='help/Python.html', params='', query='', fragment='')

    '''
    p = urlparse(url)
    conn = httplib.HTTPConnection(p.netloc)
    conn.request('HEAD', p.path)
    resp = conn.getresponse()
    return resp.status < 400


def get_category(category_name, desc='', icon='', append=False):
    """getter/setter function which creates or gets the category from the model

    :param category_name: string
    :param desc: string
    :param icon: image
    :param append: boolean, defaults to false, if false, deletes all existing pages from category
    :return: Category object
    """

    # check to see if the category exists
    if Category.objects.filter(name=category_name):
        c = Category.objects.get(name=category_name)
        if not append:
            Page.objects.filter(category=c).all().delete()
    else:
        # create the category in the models/db
        c = Category(name=category_name, icon=icon, desc=desc, is_shown=True)
        c.save()
    return c


def populate_pages(url_list, category):
    """

    :param url_list: a list of the urls for the pages that are going to be populated
    :param category: the category in which the pages fall into
    :return:
    """

    #For each url in the url_list
    for url in url_list:

        # create PageCapture object - specify the browser to be 800 x 600.
        pc = PageCapture(url,800, 600)
        url_file_name = convert_url_to_filename(url)+'.png'
        image_file_name = os.path.join(os.getcwd(), 'imgs', url_file_name)
        pc.load_url(url)
        # fetch the screen-shot
        pc.take_screen_shot(image_file_name)
        # get the title
        title = pc.get_page_title()
        # create page in models/db with category
        p = Page(category=category, title=title, is_shown=True, url=url, screenshot =image_file_name)
        p.save()
        print 'Page title= ' + p.title + ' has been saved!'


def main(file_name, category_name, append):
    """

    :param file_name:
    :param category_name:
    :param append:
    args:
        filename: takes in a filename containing a list of urls
        category_name: takes in a category_name
        append: default is true, if false delete all the pages in the category
    :return:
    """

    # read in file - store in a list (url_list)
    url_list = read_in_urls(file_name)
    # check to see if the category exists
    # create the category in the models/db
    c = get_category(category_name)
    #For each url in the url_list
        # fetch the screen-shot
        # get the title
        # create page in models/db with category
    populate_pages(url_list, c)


if __name__ == "__main__":
    import doctest
    test_results = doctest.testmod()
    print test_results
    if not test_results.failed:
        main('/Users/arazzouk/Images/eng/urls.txt','engineering',False)