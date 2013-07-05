import ifind.common.utils
import string
from ifind.common.pagecapture import PageCapture
from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)
from ifind.models.game_models import Page, Category
import os
from django.core.files import File
import httplib
from urlparse import urlparse
from ifind.common.utils import convert_url_to_filename, read_in_urls


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
        # To change to accomodate for the new changes
        image_file_name = os.path.join(os.getcwd(), 'imgs', url_file_name)
        pc.load_url(url)
        # fetch the screen-shot
        pc.take_screen_shot(image_file_name)
        # get the title
        title = pc.get_page_title()
        # create page in models/db with category
        p = Page(category=category, title=title, is_shown=True, url=url, screenshot='/imgs/'+url_file_name)
        p.save()
        print 'Page title= ' + p.title + ' has been saved!'


def populate(file_name, category_name, append):
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

import argparse


def main():

    parser = argparse.ArgumentParser(description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=int,default=False, help="")
    parser.add_argument("-cn", "--category_name", type=str, default='engineering', help="The name of the category")
    parser.add_argument("-fn", "--file_name",default= os.getcwd() + '/data/urls.txt', type=str, help="The name of the file where the urls are stored in")

    args = parser.parse_args()
    if not args.file_name and args.category_name:
        parser.print_help()
        return 2

    else:
        import doctest
        test_results = doctest.testmod()
        print test_results
        if not test_results.failed:
            populate(args.file_name, args.category_name, args.append)
            print "Category and pages have been populated"
        return 0

if __name__ == '__main__':
    main()
