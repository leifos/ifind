__author__ = 'Craig'

import os


def populate():
    # add the users for testing
    dave = User.objects.create_user('Dave', 'dave@dave.com', 'davepw')
    john = User.objects.create_user('John', 'john@john.com', 'johnpw')
    stan = User.objects.create_user('Stan', 'stan@stan.com', 'stanpw')


if __name__ == '__main__':
    print "Starting slowsearch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slowsearch_project.settings')
    from slowsearch.models import User
    populate()