__author__ = 'leif'


class GameAchievementTest(TestCase):


    def setUp(self):
        print "Setting up Game Achievements for Player Test"
        User.objects.get_or_create(username='testy', password='test')
        u = User.objects.get(username='testy')
        UserProfile.objects.get_or_create(user=u)

        Category.objects.get_or_create(name='Numbers', desc='Looking for sites that about numbers')
        c = Category.objects.get(name='Numbers')
        for pn in ['one','two','three','four']:
            Page.objects.get_or_create(category=c, title=pn, url='www.'+pn+'.com', snippet=pn, desc=('desc: ' +pn))

        Category.objects.get_or_create(name='Letters', desc='Looking for sites that  about letters')


    def test_achievements(self):

        u = User.objects.get(username='testy')
        c = Category.objects.get(name='Numbers')
        p = Page.objects.all()[0]

        cg = CurrentGame(category=c, current_page=p, user=u)

        up = User.objects.get(user=u)
        # make sure there are no highscores so far
        self.assertEquals(len(hs),0)

        gac = GameAchievementChecker(u)

        # get the lastest highscores
        hs = HighScore.object.filter(user=u)
        new_achievements_list = gac.check_and_set_new_achievements(up,hs,cg)
        # check that no achievements are awarded
        self.assertEquals(len(new_achievements_list),0)

        HighScore(user=u,category=c,highest_score=5000).save()

        hs = HighScore.object.filter(user=u)
        new_achievements_list = gac.check_and_set_new_achievements(up,hs,cg)
        # still no achievements should be awarded yet
        self.assertEquals(len(new_achievements_list),0)

        c = Category.objects.get(name='Letters')
        # add a score in for the other category
        HighScore(user=u,category=c,highest_score=1000).save()

        hs = HighScore.object.filter(user=u)
        new_achievements_list = gac.check_and_set_new_achievements(up,hs,cg)
        # the All Cats achievement is triggered
        self.assertEquals(len(new_achievements_list),1)

        # the high scores were increased
        for s in hs:
            s.highest_score += 3000
            s.save()

        new_achievements_list = gac.check_and_set_new_achievements(up,hs,cg)
        # The high scorer achievement is triggered
        self.assertEquals(len(new_achievements_list),1)
