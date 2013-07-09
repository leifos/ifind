__author__ = 'leif'
import json
import os
import sys
from ifind.common.pagecapture import PageCapture
from ifind.models.game_models import Page, Category
from ifind.common.utils import convert_url_to_filename, read_in_urls

sys.path.append(os.getcwd())
from configuration import DATA_DIR


def set_page_list(game, page_list):
    game.page_list = json.dumps(page_list)
    print game.page_list


def get_page_list(game):
    if game.page_list:
        page_list = json.loads(game.page_list)
        return page_list
    else:
        return []


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
        image_file_name = os.path.join(DATA_DIR, url_file_name)
        pc.load_url(url)
        # fetch the screen-shot
        pc.take_screen_shot(image_file_name)
        # get the title
        title = pc.get_page_title()
        # create page in models/db with category
        p = Page(category=category, title=title, is_shown=True, url=url, screenshot=os.path.join('/', DATA_DIR, url_file_name))
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


def add_page_to_db(title, url, image, category):
    """ takes page details and adds a new page to the page model/db

    Args:
        title: string, the title of the page
        url: string, the url of the page
        image: string, path to the screenshot of the page
        category: the Category class
    Returns:
        None

    """


def add_category(name, description, etc ):
    """ adds a category to the category model/db
     Args:
        name: string
        description: string
        etc
    """
