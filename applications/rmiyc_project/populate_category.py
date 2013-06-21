import ifind.common.utils
import string
#from ifind.common.pagecapture import PageCapture
from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from rmiyc.models import Page, Category


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
    num = Category.objects.filter(name=category_name).count()
    if num != 0:
        c = Category.objects.get(name=category_name)
        if not append:
            Page.objects.filter(category=c).all().delete()
    else:
        c = Category(name=category_name, icon="", desc="I am category", is_shown=True)
        c.save()
    #For each url in the url_list
    for url in url_list:
        print url.strip()
        print '              '
        # convert the url to a filename
        url_file_name = category_name + '/' + convert_url_to_filename(url.strip()) + '.png'
        print url_file_name
        # fetch the screen-shot
            # PageCapture

        # get the title
            # PageCapture
        title = 'my title '
        desc = 'page description'
        # create page in models/db with category
        Page(category=c, title=title, desc=desc, is_shown=True, url=url, screenshot=None).save()

if __name__ == "__main__":
    main('/Users/arazzouk/Images/Adam/urls-1.txt','business',True)