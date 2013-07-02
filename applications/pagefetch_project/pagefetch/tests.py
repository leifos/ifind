"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from ifind.models.game_models import Page, Category
from ifind.models.game_mechanics import GameMechanic
from django.contrib.auth.models import User
from ifind.search.engine.dummy_search import DummySearch

class PageFetchTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_page_via_admin_site(self):
        # Gertrude opens her web browser, and goes to the admin page
        self.browser.get(self.live_server_url + '/admin/')

        # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django', body.text)

        # She types in her username and passwords and hits return
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('leif')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('test')
        password_field.send_keys(Keys.RETURN)

        # her username and password are accepted, and she is taken to
        # the Site Administration page
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('administration', body.text)

        # She now sees a couple of hyperlink that says "Polls"
        #page_links = self.browser.find_elements_by_link_text('Pages')
        #self.assertEquals(len(polls_links), 2)


        # TODO: use the admin site to create a Page
        #self.fail('finish this test')

class GameModelTest(TestCase):

    def setUp(self):
        User.objects.get_or_create(username='testy', password='test')


    def test_add_cat(self):
        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that around about numbers')

        cats = Category.objects.all()
        self.assertEquals(len(cats), 1)

    def test_add_pages(self):

        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that around about numbers')[0]
        c = Category.objects.get(name='Numbers')

        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=c, title=pn, url='www.'+pn+'.com', snippet=pn, desc=('desc: ' +pn))

        page = Page.objects.all()
        self.assertEquals(len(page), 4)


class GameMechanicTest(TestCase):


    def setUp(self):
        User.objects.get_or_create(username='testy', password='test')
        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that around about numbers')
        c = Category.objects.get(name='Numbers')
        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=c, title=pn, url='www.'+pn+'.com', snippet=pn, desc=('desc: ' +pn))


    def test_game_scoring(self):
        se = DummySearch()
        u = User.objects.get(username='testy')
        c = Category.objects.get(name='Numbers')

        gm = GameMechanic(se)

        gm.create_game(u,c)
        self.assertEquals(len(gm.pages), 4)

        gm.handle_query('one')
        gm.take_points()
        gm.set_next_page()
        self.assertEquals(gm.get_current_score(),1000)


class RegistrationTest(TestCase):


    def setUp(self):
        pass


class LoginTest(TestCase):


    def setUp(self):
        pass



