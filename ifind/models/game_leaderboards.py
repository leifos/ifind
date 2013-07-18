__author__ = 'leif'

from ifind.models.game_models import HighScore, UserProfile
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
                entry['category'] = hs.category.name
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
        print highscores
        leaders = list()

        for i, hs in enumerate(highscores):
            print hs
            username = User.objects.get(id=hs['user'])

            entry = {'rank': i+1, 'username': username, 'score': hs['highest_score']}
            leaders.append(entry)

        return leaders


    def __str__(self):
        return 'Highest Overall Scores'

