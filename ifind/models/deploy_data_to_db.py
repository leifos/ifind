import os
from ifind.models.game_models import Category, Page

from configuration import MEDIA_ROOT


def get_trending_queries(filename):
    """Extract population data from a file.
       Returns a list of tuples created from comma separated values in file
    """
    f = open(filename, 'r')
    trend_tuples_list = []
    for line in f:
        trend_tuples_list.append(tuple((line.strip()).split(',')))
    f.close()
    return trend_tuples_list




def main():
    tuples_list = get_trending_queries('page_meta_data.txt')
    cat = Category.objects.get(name=tuples_list[0][0])
    for item in tuples_list:
        p = Page(category=cat, title=item[2], is_shown=True, url=item[1], screenshot=os.path.join('/', MEDIA_ROOT, item[3]))
        p.save()