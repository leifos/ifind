__author__ = 'leif'
from pagefetch_project import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.db import models
from django.contrib.auth.models import User
from ifind.models.game_models import Category, Page
from ifind.models.game_mechanics import GameMechanic
from ifind.search.engine import EngineFactory
import os
from ifind.common.setuplogger import create_ifind_logger


def handle_game_input():
    state = 0
    print '\nSkip Page (s) Take Points (t) Query (q)\n'
    ri = raw_input('Select your choice\n')
    ri = ri.lower()
    if len(ri) > 1:
        ri = ri[0]
    if ri in ['s','t']:
        state = 1
    if ri in ['q']:
        state = 2

    return state

def handle_query_input():
    ri = raw_input('Please enter your query\n')
    return ri

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')
    pass

def main():

    logger = create_ifind_logger('test_game_mech.log')
    logger.info("Program started")
    logger.info('Testing game mechanics')

    print "This script is to test the GameMechanics and interaction with the Models"

    ds = EngineFactory("Dummy")

    gm = GameMechanic(ds)
    print gm
    u = User.objects.filter(username='testy')
    if u:
        u = u[0]
    else:
        print "Adding testy user"
        u = User(username='testy',password='test')
        u.save()

    c = Category.objects.filter(name='Numbers')

    if c:
        c = c[0]
    else:
        print "Adding a Numbers Category"
        c = Category(name='Numbers', desc='Looking for sites that around about numbers')
        c.save()

    pages = Page.objects.filter(category=c)

    if not pages:
        print "Adding pages"

        for pn in ['one','two','three','four']:
            p = Page(category=c, title=pn, url='www.'+pn+'.com', snippet=pn, desc=('desc: ' +pn))
            p.save()

        pages = Page.objects.filter(category=c)

    print u
    print c
    print pages

    gm.create_game(u,c)

    print gm

    print "Game is set up to play"
    raw_input('Press enter to continue')


    while not gm.is_game_over():
        clear_screen()
        print gm
        last_query = gm.get_last_query()
        if last_query:
            print "\nLast Query: %s and Query Score: %d" % (last_query, gm.get_last_query_score())
        state = handle_game_input()
        if state == 1:
            gm.take_points()
            gm.set_next_page()
            state = 0
        if state == 2:
            query = handle_query_input()
            gm.handle_query(query)

    print '\nGame Over!!\n'
    print gm
    logger.info("Done!")

if __name__ == '__main__':
    main()
