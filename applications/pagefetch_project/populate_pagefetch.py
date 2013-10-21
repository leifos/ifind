#!/usr/bin/env python
"""
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   04/07/2013
Version: 0.1

Requires:
---------
"""
from django.core.management import setup_environ
from pagefetch_project import settings
setup_environ(settings)

from ifind.models import game_model_functions
from django.contrib.auth.models import User
from ifind.models.game_models import UserProfile, Achievement, Level
#from ifind.models import game_models
import argparse
import os


#fetch data for population from file
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

def add_achievements():
    Achievement(name='Tenderfoot', level_of_achievement=0, desc='',
                badge_icon=None, xp_earned =0).save()
    Achievement(name='Vaquero', level_of_achievement=5000, desc='',
                badge_icon=None, xp_earned =0).save()
    Achievement(name='Wrangler', level_of_achievement=25000, desc='',
                badge_icon=None, xp_earned =0).save()
    Achievement(name='Caballero', level_of_achievement=100000, desc='',
                badge_icon=None, xp_earned =0).save()

def add_levels(levels,increase):
    points = 0
    lvl = 0
    while lvl <= levels:
        Level(xp=points, level=lvl).save()
        lvl +=1
        points+=increase



#add people...
def add_players():
    jim = User(username="Jim", password='Jim')
    jane = User(username="Jane", password='Jane')
    jake = User(username="Jake", password='Jake')
    jim.save()
    jane.save()
    jake.save()
    UserProfile(user=jim, xp=760, no_games_played=8).save()
    UserProfile(user=jane, xp=2300, no_games_played=10).save()
    UserProfile(user=jake, xp=4300, no_games_played=12).save()

def main():

    parser = argparse.ArgumentParser(
        description="Populate a category and the pages associated with it")
    parser.add_argument("-a", "--append", type=int,default=True,
                        help="if set to false deletes category from database\
                        if already present.")
    #TODO(mtbvc):won't need this
    parser.add_argument("-cn", "--category_name", type=str,
                        help="Name of category.")
    parser.add_argument("-f", "--filename",
                        default= os.getcwd() + '/data/game_data.txt', type=str,
                        help="relative path to population data file")
    parser.add_argument("-l", "--lvls", default=False)

    args = parser.parse_args()
    if args.lvls:
        add_achievements()
        add_levels(50,1000)
        add_players()
        return 0
    if args.filename:
        data_list = get_trending_queries(args.filename)
        for data_tuple in data_list:
            cat=game_model_functions.get_category(data_tuple[0],'icon','',append=args.append)
            #data_tuple[1] is url
            game_model_functions.populate_pages([data_tuple[1]],cat)
        return 0
    else:
        print parser.print_help()
        return 2
        #import doctest
        #test_results = doctest.testmod()
        #print test_results
        #if not test_results.failed:
        #    populate(args.file_name, args.category_name, args.append)
        #    print "Category and pages have been populated"
        #return 0


if __name__ == '__main__':
    main()
