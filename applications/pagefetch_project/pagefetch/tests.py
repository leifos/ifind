"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""


from django.test import TestCase
from django.test import LiveServerTestCase
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
from ifind.models.game_models import Page, Category, UserProfile, Achievement
from ifind.models.game_models import CurrentGame, HighScore
from ifind.models.game_mechanics import GameMechanic
from django.contrib.auth.models import User
from ifind.search.engine import EngineFactory
from ifind.models.game_achievements import GameAchievementChecker

#from ifind.common import pagecapture
from ifind.common.setuplogger import create_ifind_logger
#from ifind.models.game_models import PlayerAchievement
from ifind.models import game_achievements

class PageFetchTest(LiveServerTestCase):

    def setUp(self):

        User.objects.get_or_create(username='leif', password='test', is_superuser=True)
        self.browser = webdriver.PhantomJS()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_page_via_admin_site(self):
        # Gertrude opens her web browser, and goes to the admin page
        print self.live_server_url
        self.browser.get(self.live_server_url + '/admin/')
        #self.browser.get("http://127.0.0.1:8000/admin/")

         # She sees the familiar 'Django administration' heading
        body = self.browser.find_element_by_tag_name('body')
        print self.browser.title
        print body.text
        self.assertIn('Django', body.text)
        print "Passed page load test"
        # She types in her username and passwords and hits return

        # She now sees a couple of hyperlink that says "Polls"
        #page_links = self.browser.find_elements_by_link_text('Pages')
        #self.assertEquals(len(polls_links), 2)
        #username_field = self.browser.find_element_by_name('username')
        #username_field.send_keys('leif')

        #password_field = self.browser.find_element_by_name('password')
        #password_field.send_keys('test')
        #password_field.send_keys(Keys.RETURN)

        # her username and password are accepted, and she is taken to
        # the Site Administration page
        #body = self.browser.find_element_by_tag_name('body')
        #self.assertIn('administration', body.text)


        # TODO: use the admin site to create a Page
        #self.fail('finish this test')


class GameModelTest(TestCase):

    def setUp(self):
        User.objects.get_or_create(username='testy', password='test')
        self.logger = create_ifind_logger('game_model_teset.log')


    def test_add_cat(self):
        self.logger.info("Testing whether the numbers cat has been successfully added")
        #print "Testing whether the numbers cat has been successfully added"
        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that around about numbers')

        cats = Category.objects.all()
        self.assertEquals(len(cats), 1)

    def test_add_pages(self):
        self.logger.info("Testing whether four pages are added to the Numbers Cat.")
        #print "Testing whether four pages are added to the Numbers Cat."
        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that around about numbers')[0]
        c = Category.objects.get(name='Numbers')

        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=c, title=pn,
                                       url='www.'+pn+'.com', snippet=pn,
                                       desc=('desc: ' +pn))

        page = Page.objects.all()
        self.assertEquals(len(page), 4)


class GameMechanicTest(TestCase):


    def setUp(self):
        self.logger = create_ifind_logger("game_mechanic_test.log")
        print "Setting up Game Mechanic Test"
        User.objects.get_or_create(username='testy', password='test')
        self.u = User.objects.get(username='testy')
        UserProfile.objects.create(user=self.u)
        Category.objects.get_or_create(
            name='Numbers', desc='Looking for sites that around about numbers')

        c = Category.objects.get(name='Numbers')
        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=c, title=pn,
                                       url='www.'+pn+'.com', snippet=pn,
                                       desc=('desc: ' +pn))


    def test_game_scoring(self):
        self.logger.info("Testing Game Scoring with a Dummy SearchEngine")
        #print "Testing Game Scoring with a Dummy SearchEngine"
        se = EngineFactory("Dummy")
        u = User.objects.get(username='testy')
        c = Category.objects.get(name='Numbers')

        gm = GameMechanic(se)
        gm.create_game(u,c)
        self.logger.info("Checking if the category Numbers has four pages.")
        #print "Checking if the category Numbers has four pages."
        self.assertEquals(len(gm.pages), 4)

        gm.handle_query('one')
        gm.take_points()
        gm.set_next_page()
        self.logger.info("Checking whether the query, one, scores 1000 points-\
                         which it should given the data and dummy search engine")
        #print "Checking whether the query, one, scores 1000 points -
        #which it should given the data and dummy search engine"
        self.assertEquals(gm.get_current_score(),1000)


class GameAchievementTest(TestCase):


    def setUp(self):


        self.logger = create_ifind_logger('test_game_achievements.log')

        #print "Setting up Game Achievements for Player Test"
        self.logger.info("Setting up Game Achievemtns for Player Test.")
        User.objects.get_or_create(username='testy', password='test')
        self.u = User.objects.get(username='testy')
        UserProfile.objects.get_or_create(user=self.u)

        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that about numbers')
        self.c = Category.objects.get(name='Numbers')
        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=self.c, title=pn, url='www.'+pn+'.com', snippet=pn, desc=('desc: ' +pn))

        Category.objects.get_or_create(name='Letters', desc='Looking for sites that  about letters')
        self.c1 = Category.objects.get(name='Letters')
        self.assertEquals(len(Category.objects.all()), 2)

        #------------
        for name in ['1', '2', '3', '4', '5', '6']:
            Category.objects.get_or_create(name=name, desc='Looking for sites that  about {0}'.format(name))

        Achievement.objects.get_or_create(name="HighScorer", desc='',xp_earned=10000, achievement_class='HighScorer')
        self.allcat = Achievement.objects.get_or_create(name="AllCat", desc='', xp_earned=500, achievement_class='AllCat')
        Achievement.objects.get_or_create(name="FivePagesInAGame", desc='', xp_earned=7, achievement_class='FivePagesInAGame')
        Achievement.objects.get_or_create(name="TenGamesPlayed", desc='', xp_earned=7, achievement_class='TenGamesPlayed')
        Achievement.objects.get_or_create(name="UberSearcher", desc='', xp_earned=7, achievement_class='UberSearcher')

        self.p = Page.objects.all()[0]
        self.cg = CurrentGame(category=self.c, current_page=self.p, user=self.u)
        self.up = UserProfile.objects.get(user=self.u)
        self.gac = GameAchievementChecker(self.u)

    def test_achievements(self):
        print "testing achievements"
        # make sure there are no highscores so far
        hs = HighScore.objects.filter(user=self.u)
        self.assertEquals(len(hs),0)
        # get the latest highscores
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        # check that no achievements are awarded
        self.assertEquals(len(new_achievements_list),0)
        HighScore(user=self.u,category=self.c,highest_score=2900).save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        # still no achievements should be awarded yet
        self.assertEquals(len(new_achievements_list),0)

    def test_all_cats(self):
        # add a score in for the other category
        for cat in Category.objects.all():
            HighScore(user=self.u,category=cat ,highest_score=1000).save()

        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up, hs,self.cg)
        # the All Cats achievement is triggered
        self.assertEquals(new_achievements_list[0].achievement, self.allcat[0])

    def test_highscorer(self):
        HighScore(user=self.u,category=self.c,highest_score=9000).save()
        hs = HighScore.objects.filter(user=self.u)
        total =0
        for h in hs:
            total += hs[0].highest_score
        print("testing highscorer\nTotal score:{0}".format(total))
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up, hs,self.cg)
        # The Ubersearcher achievement is triggered
        self.assertEquals(len(new_achievements_list), 1)
        # the high scores were increased
        hs = HighScore.objects.filter(user=self.u)
        for s in hs:
            s.highest_score += 3000
            s.save()
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up, hs,self.cg)
        # The high scorer achievement is triggered
        self.assertEquals(len(new_achievements_list),1)

    def test_fives_pages_in_game(self):
        #testing FivePagesInAGame achievemnt class
        # add a score in for the other category
        HighScore(user=self.u,category=self.c,most_no_pages_found=2).save()
        hs = HighScore.objects.filter(user=self.u)

        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        #should not trigger achievement
        self.assertEquals(len(new_achievements_list),0)

        HighScore(user=self.u,category=self.c,most_no_pages_found=5).save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        #should trigger FivePagesInAGame achievement
        self.assertEquals(len(new_achievements_list),1)

    def test_ten_games_played(self):
        #Test TenGamesPlayed
        # add a score in for the other category
        self.up.no_games_played = 9
        self.up.save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        #should not trigger achievement
        self.assertEquals(len(new_achievements_list),0)

        # add a score in for the other category
        self.up.no_games_played = 10
        self.up.save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        #should trigger achievement
        self.assertEquals(len(new_achievements_list),1)

    def test_uber_searcher(self):
        #Test UberSearcher
        # add a score in for the other category
        HighScore(user=self.u,category=self.c, highest_score=2000).save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        #should not trigger achievement
        self.assertEquals(len(new_achievements_list),0)

        # add a score in for the other category
        HighScore(user=self.u,category=self.c, highest_score=3000).save()
        hs = HighScore.objects.filter(user=self.u)
        new_achievements_list = self.gac.check_and_set_new_achievements(self.up,hs,self.cg)
        self.assertEquals(len(new_achievements_list),1)







#class RegistrationTest(TestCase):
#    #TODO(mtbvc):...
#
#
#    def setUp(self):
#        pass
#
#
#class LoginTest(TestCase):
#
#
#    def setUp(self):
#        pass
#
#

