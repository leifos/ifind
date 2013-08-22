__author__ = 'arazzouk'
from ifind.models.game_models import Page ,Category, UserProfile
import os
import sys
sys.path.append(os.getcwd())


def get_findability_score():
    pages = Page.objects.all()
    f = open('findability.txt', 'a')
    for p in pages:
        if p.no_of_queries_issued != 0:
            finability = p.no_times_retrieved / p.no_of_queries_issued
            url = p.url
            f.write('%d,%s\n' % (finability, url))


def calculate_game_played_no():
    pass


def get_players_ages():
    pass




get_findability_score()