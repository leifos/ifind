__author__ = 'leif'
import json


def set_page_list(game, list):
    game.page_list = json.dumps(list)
    print game.page_list

def get_page_list(game):
    if game.page_list:
        list = json.loads(game.page_list)
        return list
    else:
        return []

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