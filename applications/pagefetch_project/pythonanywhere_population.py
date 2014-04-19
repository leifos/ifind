#!/usr/bin/env python
"""
A quick population script for testing rmiyc app
Populates the database with sample data

Run populate_category.py before running this script!

=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   24/02/2014
"""
#from ifind.models import game_model_functions
from pagefetch_project import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.contrib.auth.models import User
from ifind.models.game_models import UserProfile, Achievement, Level, HighScore, Category, PlayerAchievement
from configuration import STATIC_PATH
import os

def achievements():
    Achievement.objects.get_or_create(name="HighScorer", desc='',xp_earned=10000, achievement_class='HighScorer', badge_icon='badges/medal2.png')
    Achievement.objects.get_or_create(name="AllCat", desc='', xp_earned=500, achievement_class='AllCat', badge_icon='badges/medal2.png')
    Achievement.objects.get_or_create(name="FivePagesInAGame", desc='', xp_earned=7, achievement_class='FivePagesInAGame', badge_icon='badges/medal2.png')
    Achievement.objects.get_or_create(name="TenGamesPlayed", desc='', xp_earned=7, achievement_class='TenGamesPlayed', badge_icon='badges/medal2.png')
    Achievement.objects.get_or_create(name="UberSearcher", desc='', xp_earned=7, achievement_class='UberSearcher', badge_icon='badges/medal2.png')


def players():
    anon = User(username="anon")
    jim = User(username="Jimmy")
    jane = User(username="Jane")
    jake = User(username="Jake")
    jim.set_password("test")
    jane.set_password("test")
    jake.set_password("test")
    anon.save()
    jim.save()
    jane.save()
    jake.save()
    UserProfile(user=anon, xp=0, no_games_played=0).save()
    UserProfile(user=jim, xp=760, no_games_played=8).save()
    UserProfile(user=jane, xp=2300, no_games_played=10).save()
    UserProfile(user=jake, xp=4300, no_games_played=12).save()


def highscores():
    HighScore(user=User.objects.filter(username='Jimmy')[0],category=Category.objects.filter(name="Films")[0],highest_score=2566).save()
    HighScore(user=User.objects.filter(username='Jimmy')[0],category=Category.objects.filter(name="Actors")[0],highest_score=3200).save()
    HighScore(user=User.objects.filter(username='Jane')[0],category=Category.objects.filter(name="Films")[0],highest_score=1420).save()
    HighScore(user=User.objects.filter(username='Jake')[0],category=Category.objects.filter(name="Games")[0],highest_score=1667).save()
    HighScore(user=User.objects.filter(username='Jimmy')[0],category=Category.objects.filter(name="Universities")[0],highest_score=500).save()
    HighScore(user=User.objects.filter(username='Jake')[0],category=Category.objects.filter(name="Films")[0],highest_score=179).save()
    HighScore(user=User.objects.filter(username='Jane')[0],category=Category.objects.filter(name="Actors")[0],highest_score=800).save()
    HighScore(user=User.objects.filter(username='Jake')[0],category=Category.objects.filter(name="Actors")[0],highest_score=700).save()


def player_achievements():
    jim = User.objects.filter(username='Jimmy')
    ac2 = Achievement.objects.filter(name="UberSearcher")
    PlayerAchievement(user=jim[0], achievement=ac2[0]).save()


def main():
    achievements()
    print("populated achievements")
    players()
    print ("populated players")
    highscores()
    print("populated hs")
    player_achievements()
    print("populated pl_achievements")


if __name__ == '__main__':
    main()
