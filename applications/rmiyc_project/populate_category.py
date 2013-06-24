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
    """Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in url if c in valid_chars)
    filename = filename.replace(' ','_') # to remove spaces in file names.
    return filename


def read_in_urls(filename):

    ## Open the file with read only permit
    f = open(filename,'r')
    ## Read the first line
    print 'file is opened'
    url_list = []
    for line in f:
        url_list.append(line)

    f.close()
    return url_list


def get_category(category_name, desc='', icon='', append=False):
    if Category.objects.filter(name=category_name):
        c = Category.objects.get(name=category_name)
        if not append:
            Page.objects.filter(category=c).all().delete()
    else:
        c = Category(name=category_name, icon=icon, desc=desc, is_shown=True)
        c.save()
    return c


def populate_page():
    pass


def fetch_screen_shot():
    pass


def get_page_title():
    pass



def main(file_name, category_name, append):
    """
    args:
        filename: takes in a filename containing a list of urls
        category_name: takes in a category_name
        append: default is true, if false delete all the pages in the category
    :return:
    """

    # create PageCapture object - specify the browser to be 800 x 600.

    # read in file - store in a list (url_list)
    url_list = read_in_urls(file_name)
    # check to see if the category exists,
        # create the category in the models/db
    c = get_category(category_name)
    #For each url in the url_list
    obj=PageCapture(800,600)
    for url in url_list:
        # convert the url to a filename os.path.join()
        url_file_name = convert_url_to_filename(url.strip())+'.png'
        obj.get_webpage(url)
        # fetch the screen-shot
            # PageCapture
        obj.take_screen_shot(url,'~/code/applications/rmiyc_project/imgs/',url_file_name,600,800)
        # get the title
            # PageCapture
        title = obj.get_page_title()
        # create page in models/db with category
        Page(category=c, title=title, is_shown=True, url=url, screenshot ='/imgs/'+url_file_name).save()
        print 'Page title= ' + title + '       has been saved!'

if __name__ == "__main__":
    main('/Users/arazzouk/Images/Adam/urls-1.txt','bu',False)