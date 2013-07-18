__author__ = 'leif'

from ifind.models.game_models import HighScore, UserProfile
from django.contrib.auth.models import User

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
            leaders.append({'rank': i+1, 'username': hs.user.username, 'category': hs.category.name, 'score': hs.highest_score})

        return leaders


class HighScoresLeaderboard(GameLeaderboard):

    def get_leaderboard(self):
        hs = HighScore.objects.all().order_by('highest_score')[:self.top]
        return self.highscore_to_list(hs)




