__author__ = 'leif'
from pagefetch_project import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.db import models
from django.contrib.auth.models import User
from ifind.models.game_models import Category, Page
from ifind.models.game_mechanics import GameMechanic
import os

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
    #if os.name == 'nt':
        #os.system('cls')
    #else:
        #os.system('clear')
    pass

def main():


    print "This script is to test the GameMechanics and interaction with the Models"

    gm = GameMechanic()
    print gm
    u = User.objects.filter(username='test user')
    if u:
        u = u[0]
    else:
        print "Adding a test user"
        u = User(username='test user',password='test').save()

    c = Category.objects.filter(name='test cat')

    if c:
        c = c[0]
    else:
        print "Adding a test cat"
        c = Category(name='test cat', desc='pages in test cat')
        c.save()

    pages = Page.objects.filter(category=c)

    if not pages:
        print "Adding pages"

        for pn in ['one','two','three','four']:
            p = Page(category=c, title=pn, url='www.test.com', snippet=pn, desc=('desc: ' +pn))
            p.save()

        pages = Page.objects.filter(category=c)

    print u
    print c
    print pages

    print pages.get(id=5)


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

    print '\nGame Over\n'
    print gm


if __name__ == '__main__':
    main()