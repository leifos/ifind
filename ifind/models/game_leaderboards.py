__author__ = 'leif'

from ifind.models.game_models import HighScore, UserProfile
from ifind.common.utils import encode_string_to_url
from django.contrib.auth.models import User
from django.db.models import Max, Sum, Avg


# ranking based on highest total score (top x players)
# ranking of players based on level/xp
# top players in each category
# top schools ranked by average total_score of players
# boys vs girls based on average total_score
# and breakdown by age / boys vs girls
# add in school, gender, age, into UserProfile
# ranking based on the last 30 days / highest scores


class GameLeaderboard(object):

    def __init__(self, top=20):
        self.top = top


    def get_leaderboard(self):
        pass

    def highscore_to_list(self, highscores):
        """
        :param highscores: list of rows from HighScore
        :return: a formatted list rank, username, uid, category, cid, highest_score
        """

        leaders = list()

        for i, hs in enumerate(highscores):

            entry = {'rank': i+1, 'username': hs.user.username, 'score': hs.highest_score}
            if hs.category:
                print hs.category
                entry['category'] = hs.category.name
                entry['category_url'] = encode_string_to_url(hs.category.name)
            print entry
            leaders.append(entry)

        return leaders


class CatHighScoresLeaderboard(GameLeaderboard):

    def get_leaderboard(self):
        hs = HighScore.objects.all().order_by('-highest_score')[:self.top]
        return self.highscore_to_list(hs)

    def __str__(self):
        return 'Highest Category Scores'

class HighScoresLeaderboard(GameLeaderboard):

    def get_leaderboard(self):
        highscores = HighScore.objects.values('user').annotate(highest_score=Sum('highest_score')).order_by('-highest_score')[:self.top]

        leaders = list()

        for i, hs in enumerate(highscores):
            username = User.objects.get(id=hs['user'])

            entry = {'rank': i+1, 'username': username, 'score': hs['highest_score']}
            leaders.append(entry)

        return leaders


    def __str__(self):
        return 'Highest Overall Scores'










class SchoolLeaderboard(GameLeaderboard):

    def get_leaderboard(self, user):
        usr = User.objects.get(username=user.username)
        if usr.username != '':
            viewer_profile = UserProfile.objects.get(user=usr)
            viewer_school = viewer_profile.school
            #get all viewer's school mates
            profiles = UserProfile.objects.filter(school=viewer_school)

            hs = []
            score_list = []
            for profile in profiles:
                hs = HighScore.objects.filter(user=viewer_profile.user)
                Sum=0
                for item in hs:
                    Sum += item.highest_score
                dummy_hs = HighScore(user=profile.user, highest_score=Sum, category=None)
                score_list.append(dummy_hs)

            #hs.order_by('-highest_score')[:self.top]
        #hs = HighScore.objects.all().order_by('-highest_score')[:self.top]
            return self.highscore_to_list(score_list)

    def __str__(self):
        return 'School High Scores'

