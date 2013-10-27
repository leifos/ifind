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


def main():
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
