import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "slowsearch_project.settings")

import time
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User
from utils import run_query

inappropriate_names = ['fuck', 'tits', 'ass']


class UserRegTests(TestCase):

    def test_for_inappropriate_language(self):
        new_user = User.objects.create_user(username='fuckwit', email='test@test.com', password='test')

        inappropriate = False

        for n in inappropriate_names:
            if n in new_user.username:
                inappropriate = True
                break

        self.assertFalse(inappropriate)

    # tests that condition logic is applied correctly to users
    # if test passes then condition logic is applied correctly, alternating between A and B for each new user
    def test_condition(self):
        new_user1 = User.objects.create_user(username='user1', email='test1@test.com', password='test')
        new_user2 = User.objects.create_user(username='user2', email='test2@test.com', password='test')
        new_user3 = User.objects.create_user(username='user3', email='test3@test.com', password='test')
        new_user4 = User.objects.create_user(username='user4', email='test4@test.com', password='test')

        new_user_list = [new_user1, new_user2, new_user3, new_user4]

        cnd_A_count = 0
        cnd_B_count = 0

        for n in new_user_list:
            if n.id % 2 == 0:
                cnd_A_count += 1
            elif n.id % 2 != 0:
                cnd_B_count += 1

        assertion = (cnd_A_count != 0 and cnd_B_count != 0 and cnd_A_count == cnd_B_count)

        self.assertTrue(assertion)


class SearchTests(TestCase):
    def test_delay(self):
        start = time.time()
        r = run_query('test', 2)
        end = time.time()

        time_elapsed_delay = end-start

        start = time.time()
        r = run_query('test', 1)
        end = time.time()

        time_elapsed_no_delay = end-start

        self.assertTrue(time_elapsed_delay >= 5 and time_elapsed_delay > time_elapsed_no_delay)






