import os
import sys

from rmiyc_project import settings
from django.core.management import setup_environ
setup_environ(settings)

def read_in_file(filename):
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
    print 'Populating the Database from page_meta_data.txt'
    print '************************************************'

    from ifind.models.game_models import Category, Page
    from configuration import MEDIA_ROOT,STATIC_PATH
    from ifind.common.utils import convert_url_to_filename

    tuples_list = read_in_file('page_meta_data.txt')
    c = Category(name="research", icon=os.path.join(STATIC_PATH,'imgs/research.jpg'), desc=None, is_shown=True)
    c.save()
    c = Category(name="about glasgow", icon=os.path.join(STATIC_PATH,'imgs/about_glasgow.jpg'), desc=None, is_shown=True)
    c.save()
    c = Category(name="undergraduate", icon=os.path.join(STATIC_PATH,'imgs/undergraduate.jpg'), desc=None, is_shown=True)
    c.save()
    c = Category(name="postgraduate", icon=os.path.join(STATIC_PATH,'imgs/postgraduate.jpg'), desc=None, is_shown=True)
    c.save()
    c = Category(name="alumni", icon=os.path.join(STATIC_PATH,'imgs/alumni.png'), desc=None, is_shown=True)
    c.save()
    c = Category(name="student life", icon= os.path.join(STATIC_PATH,'imgs/student_life.jpg'), desc=None, is_shown=True)
    c.save()
    for item in tuples_list:
            cat = Category.objects.get(name=item[0])
            url_file_name = convert_url_to_filename(item[1])+'.png'
            p = Page(category=cat, title=item[2], is_shown=True, url=item[1],screenshot=os.path.join('/', MEDIA_ROOT, url_file_name))
            p.save()
            print("page with"+ item[2] +"has been saved")

if __name__ == "__main__":
    main()


