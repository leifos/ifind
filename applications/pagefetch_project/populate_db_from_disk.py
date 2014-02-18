#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   27/10/2013

Requires:
---------
"""
import sys
from django.core.management import setup_environ
from pagefetch_project import settings
setup_environ(settings)

from ifind.models.game_models import Page
from ifind.common.utils import get_trending_queries
from ifind.models import game_model_functions

from ifind.models.game_model_functions import populate


from configuration import  STATIC_PATH
import os


def populate_cats():
    game_model_functions.get_category('Space Objects', 'data/cat_images/the25.png','SpaceObjects',append=True)
    game_model_functions.get_category('Actors', 'data/cat_images/oscars.png', 'Actors', append=True)
    game_model_functions.get_category('Musical Artists','data/cat_images/dj1.png','MusicalArtists',append=True)
    game_model_functions.get_category('Films', 'data/cat_images/clapper.png','Films',append=True)
    game_model_functions.get_category('Games', 'data/cat_images/games4.png','Games',append=True)
    game_model_functions.get_category('Kids TV', 'data/cat_images/television4.png','KidsTV',append=True)
    game_model_functions.get_category('Business People', 'data/cat_images/career.png','BusinessPeople',append=True)
    game_model_functions.get_category('Universities', 'data/cat_images/university2.png','Universities',append=True)




def main():
    populate_cats()
    #split line into tokens
    meta_data_file = sys.argv[1]
    data_list = get_trending_queries(meta_data_file)
    for data_tuple in data_list:
        cat = game_model_functions.get_category(data_tuple[0],'icon','',append=True)
        p = Page(category=cat, title=data_tuple[2], is_shown=True, url=data_tuple[1], screenshot=data_tuple[3])
        p.save()
    return 0


if __name__ == "__main__":
    sys.exit(main())
