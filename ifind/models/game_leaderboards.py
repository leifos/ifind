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

    def get_leaderboard(self):
        users = UserProfile.objects.all()
        schools = {}
        score_list=[]
        for user in users:
            if user.school != "":
                if user.school not in schools:
                    user_score = self._get_user_score_sum(user)
                    #list is [total_score_of_users,num_of_users]
                    schools[user.school] = [user_score,1]
                else:
                    schools[user.school][0] += self._get_user_score_sum(user)
                    schools[user.school][1] += 1
        for school, values in schools.iteritems():
            dummy_user = User(username=school)
            score_list.append(HighScore(user=dummy_user, highest_score=values[0]/values[1] ,category=None ))
            score_list.sort(key=lambda x: x.highest_score, reverse=True)
        return self.highscore_to_list(score_list)

    def _get_user_score_sum(self, user):
        hs = HighScore.objects.filter(user=user.user)
        user_score = 0
        for sc in hs:
            user_score += sc.highest_score
        return user_score

    def __str__(self):
        return 'School High Scores'











class AgeLeaderboard(GameLeaderboard):

    def get_leaderboard(self, user):
        if user.username == '':
            return None
        usr = User.objects.get(username=user.username)
        if usr.username != '':
            viewer_profile = UserProfile.objects.get(user=usr)
            viewer_age = viewer_profile.age
            #get all in user's age group
            profiles = UserProfile.objects.filter(age=viewer_age)
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
        return 'High Scores by age group'








class GenderLeaderboard(GameLeaderboard):

    def get_leaderboard(self, user):
        if user.username == '':
            return None
        usr = User.objects.get(username=user.username)
        if usr.username != '':
            viewer_profile = UserProfile.objects.get(user=usr)
            viewer_gender = viewer_profile.gender
            #get all in user's age group
            profiles = UserProfile.objects.filter(gender=viewer_gender)
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
        return 'High Scores by gender group'

