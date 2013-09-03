__author__ = 'leif'
from ifind.asg.abstract_search_game import ABSGame
from ifind.asg.asg_generator import RandomYieldGenerator, TestHighYieldGenerator, ConstantLinearYieldGenerator, TestYieldGenerator, CueGenerator
from ifind.search.cache import RedisConn
from django.contrib.auth.models import User
from models import UserProfile, MaxHighScore, GameExperiment
import datetime
from keys import REDIS_STR, REDIS_PW, REDIS_PORT
from django.core.cache import cache
import pickle

ryg = RandomYieldGenerator()
tyg = TestYieldGenerator()
cyg = ConstantLinearYieldGenerator()
hyg = TestHighYieldGenerator()
cg = CueGenerator(cue_length=60)

random_game = {'yield_generator': ryg, 'cue_generator': cg, 'query_cost': 2, 'assess_cost': 1 }
high_game = {'yield_generator': hyg, 'cue_generator': cg, 'query_cost': 2, 'assess_cost': 1 }
test_game = {'yield_generator': tyg, 'cue_generator': cg, 'query_cost': 2, 'assess_cost': 1 }
low_cost_game = {'yield_generator': hyg, 'cue_generator': cg, 'query_cost': 1, 'assess_cost': 2 }


game_types = [random_game, random_game, high_game, test_game, low_cost_game]



def create_and_start_game(num):
    gt = game_types[0]
    if (num < len(game_types)):
        gt = game_types[num]

    game = ABSGame(gt['yield_generator'],gt['cue_generator'],cq=gt['query_cost'],ca=gt['assess_cost'], id=num)
    game.start_game()
    return game

def store_game_incache(id, game):
    cache.set(id,pickle.dumps(game), 500)

def get_game_incache(id):
    game = pickle.loads(cache.get(id))
    return game

def get_redis_connection():
    rc = RedisConn(host=REDIS_STR, port=REDIS_PORT, password=REDIS_PW)
    rc.connect()
    return rc

def retrieve_game(id):
    return get_game_incache(id)
    #rc = get_redis_connection()
    #return rc.get(id)


def store_game(id, game):
    store_game_incache(id, game)
    #rc = get_redis_connection()
    #rc.store(id, game)


def end_game(user, game):
    update_user_profile(user, game)
    new_high = update_high_scores(user, game)
    update_game_experiment(game)
    return new_high

def update_user_profile(user, game):
    up = user.get_profile()
    up.last_time_played = datetime.datetime.now()
    up.no_games_played = up.no_games_played + 1
    up.no_queries_issued = up.no_queries_issued + game.queries_issued
    up.no_docs_assessed = up.no_docs_assessed + game.docs_assessed
    up.total_points = up.total_points + game.points
    up.total_tokens = up.total_tokens + game.tokens_spent
    up.save()


def update_high_scores(user, game):
    """ creates a new high score if there was no previous high score for this game type
    if a high score exists, checks to see if the high score has been beaten
    if so, updates the highscore record.
    :param user: django user model
    :param game: ABSGame
    :return: True if high was updated, else false (ie. score is not a new high score)
    """
    ge = GameExperiment.objects.get(config=game.id)
    mhsl = MaxHighScore.objects.filter(user=user, game_experiment=ge)
    mhs = None
    if mhsl:
        mhs = mhsl[0]

    if mhs:
        #update MaxHighScore if appropriate
        if game.points > mhs.points:
            mhs.points = game.points
            mhs.save()
            return True
        else:
            return False

    else:
        # create MaxHighScore
        mhs = MaxHighScore(user=user, game_experiment=ge, points=game.points)
        mhs.save()
        return True

def update_game_experiment(game):
    ge = GameExperiment.objects.get(config=game.id)
    ge.times_played = ge.times_played + 1
    ge.no_queries_issued = ge.no_queries_issued + game.queries_issued
    ge.no_docs_assessed = ge.no_docs_assessed + game.docs_assessed
    ge.total_points = ge.total_points + game.points
    ge.total_tokens = ge.total_tokens + game.tokens_spent
    if game.points > ge.best_so_far:
        ge.best_so_far = game.points

    ge.save()
