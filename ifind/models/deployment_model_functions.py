import json
import os
import sys
from ifind.common.pagecapture import PageCapture
from ifind.models.game_models import Page, Category
from ifind.common.utils import convert_url_to_filename, read_in_urls


sys.path.append(os.getcwd())
from configuration import DATA_DIR
from configuration import MEDIA_ROOT

#from rmiyc_project import settings
#from django.core.management import setup_environ
#setup_environ(settings)

def set_page_list(game, page_list):
    game.page_list = json.dumps(page_list)
    print game.page_list


def get_page_list(game):
    if game.page_list:
        page_list = json.loads(game.page_list)
        return page_list
    else:
        return []


def get_category(category_name, icon, desc ,append=False):
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


def populate_pages(url_list, category, halved_screen_shot=False):
    """

    :param url_list: a list of the urls for the pages that are going to be populated
    :param category: the category in which the pages fall into
    :return:
    """

    #For each url in the url_list
    f = open('page_meta_data.txt','a')
    for url in url_list:

        # create PageCapture object - specify the browser to be 800 x 600.
        try:
            pc = PageCapture(url,800, 600)
            url_file_name = convert_url_to_filename(url)+'.png'
            # To change to accomodate for the new changes
            image_file_name = os.path.join(DATA_DIR, url_file_name)
            pc.load_url(url)
            # fetch the screen-shot
            if halved_screen_shot:
                pc.crop_screen_shot(image_file_name,0,0,1000,1000)
                #pc.halve_screen_shot(image_file_name)
            else:
                pc.take_screen_shot(image_file_name)

            # get the title
            title = pc.get_page_title()
            # create page in models/db with category
            # Abdullah , using DATA_DIR did not work for me because it uses the current working directory in the url.

            #save to file instead of db here to decouple.
            f.write('%s,%s,%s,%s\n' % (category.name, url, title,image_file_name))




            #p = Page(category=category, title=title, is_shown=True, url=url, screenshot=os.path.join('/', MEDIA_ROOT, url_file_name))
            #p.save()
            #print 'Page title= ' + p.title + ' has been saved!'

        except ValueError:
            print 'Page  has ((NOT)) been saved!'
            print 'ERROR IS'
            print ValueError
            continue
    f.close()


def populate(file_name, category_name, append, halved_screen_shot, icon='', desc=''):
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
    c = get_category(category_name,icon,desc)
    #For each url in the url_list
        # fetch the screen-shot
        # get the title
        # create page in models/db with category
    populate_pages(url_list, c, halved_screen_shot)
