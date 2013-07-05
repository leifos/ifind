#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   04/07/2013
Version: 0.1

Requires:
---------
"""
from ifind.models.game_models import Category #,Page


def build_categories(cat_name, cat_description, trend_name):
    """Add categories to database."""
    # check to see if the category exists
    if Category.objects.filter(name=cat_name):
        c = Category.objects.get(name=cat_name)
        #if not append:
        #    Page.objects.filter(category=c).all().delete()
    else:
        # create the category in the models/db
        c = Category(name=cat_name, desc=cat_description, is_shown=True)
        c.save()
    return c

def add_pages(cat_name, url, rank):
    """Add page and related data to database."""
    """

    :param url_list: a list of the urls for the pages that are going to be populated
    :param category: the category in which the pages fall into
    :return:
    """

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


        """



#########
def add_achievements():
    pass

def add_levels():
    pass

#add people... put these functions in another file?

