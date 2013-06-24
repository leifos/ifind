import ifind.common.utils
import string
from ifind.common.pagecapture import PageCapture
from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from rmiyc.models import Page, Category
import os
from django.core.files import File


def convert_url_to_filename(url):
    """Take a url string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    >>> convert_url_to_filename("http://www.google.com")
    'www-google-com'
    >>> convert_url_to_filename("http://www.dcs.gla.ac.uk/~leif/index.html")
    'www-dcs-gla-ac-uk-leif-index-html'
    >>> convert_url_to_filename("www.ball.com/dj")
    'www-ball-com-dj'
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in url if c in valid_chars)
    filename = filename.replace(' ','_') # to remove spaces in file names.
    return filename


def read_in_urls(filename):
    # read in file - store in a list (url_list)
    ## Open the file with read only permit
    f = open(filename, 'r')
    ## Read the first line
    print 'file is opened'
    url_list = []
    for line in f:
        # clean up the url
        url = line.strip()
        # validate the url
        # is it a well-formed url string
        url_list.append(url)

    f.close()
    print 'file is closed'
    return url_list


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

    :param url_list:
    :param category:
    :return:
    """
    # create PageCapture object - specify the browser to be 800 x 600.

    #For each url in the url_list
    for url in url_list:
        # convert the url to a filename os.path.join()
        # This added a back slash / at the end of the url which caused problems
        # Strip urls from spaces

        pc = PageCapture(url,800, 600)
        url_file_name = convert_url_to_filename(url)+'.png'
        image_file_name = os.path.join(os.getcwd(),'imgs',url_file_name)
        print image_file_name
        pc.load_url(url)
        # fetch the screen-shot
        pc.fetch_screen_shot(image_file_name)
        # get the title
        title = pc.get_page_title()
        # create page in models/db with category
        Page(category=category, title=title, is_shown=True, url=url, screenshot =image_file_name).save()
        print 'Page title= ' + title + ' has been saved!'




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
    main('/Users/arazzouk/Images/eng/urls.txt','engineering',False)