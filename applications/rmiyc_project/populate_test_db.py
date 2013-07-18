#!/usr/bin/env python
"""
A quick population script for testing rmiyc app
Populates the database with sample data
=============================
Author: mtbvc <1006404b@student.gla.ac.uk>
Date:   18/07/2013
Version: 0.1
"""
#from ifind.models import game_model_functions
from django.contrib.auth.models import User
from ifind.models.game_models import UserProfile, Achievement, Level, HighScore, Category

class Populate:

    def achievements(self):
        Achievement.objects.get_or_create(name="HighScorer", desc='',xp_earned=10000, achievement_class='HighScorer')
        Achievement.objects.get_or_create(name="AllCat", desc='', xp_earned=500, achievement_class='AllCat')
        Achievement.objects.get_or_create(name="FivePagesInAGame", desc='', xp_earned=7, achievement_class='FivePagesInAGame')
        Achievement.objects.get_or_create(name="TenGamesPlayed", desc='', xp_earned=7, achievement_class='TenGamesPlayed')
        Achievement.objects.get_or_create(name="UberSearcher", desc='', xp_earned=7, achievement_class='UberSearcher')


    def levels(self,levels,increase):
        points = 0
        lvl = 0
        while lvl <= levels:
            Level(xp=points, level=lvl).save()
            lvl +=1
            points+=increase

    def players(self):
        jim = User(username="Jim")
        jane = User(username="Jane")
        jake = User(username="Jake")
        jim.set_password("test")
        jane.set_password("test")
        jake.set_password("test")   
        jim.save()
        jane.save()
        jake.save()
        UserProfile(user=jim, xp=760, no_games_played=8).save()
        UserProfile(user=jane, xp=2300, no_games_played=10).save()
        UserProfile(user=jake, xp=4300, no_games_played=12).save()


    def categories(self):
        Category.objects.get_or_create(name='Undergraduate', desc='Looking for sites that around about numbers')
        Category.objects.get_or_create(name='Postgraduate', desc='Looking for sites that around about numbers')
        Category.objects.get_or_create(name='Alumni', desc='Looking for sites that around about numbers')
        Category.objects.get_or_create(name='Research', desc='Looking for sites that around about numbers')
        Category.objects.get_or_create(name='StudentLife', desc='Looking for sites that around about numbers')



    def highscores(self):
        HighScore(user=User.objects.filter(username='Jim')[0],category=Category.objects.filter(name="Undergraduate")[0],highest_score=100000).save()
        HighScore(user=User.objects.filter(username='Jim')[0],category=Category.objects.filter(name="Postgraduate")[0],highest_score=10000).save()
        HighScore(user=User.objects.filter(username='Jane')[0],category=Category.objects.filter(name="Research")[0],highest_score=5000).save()
        HighScore(user=User.objects.filter(username='Jake')[0],category=Category.objects.filter(name="Undergraduate")[0],highest_score=5000).save()
        HighScore(user=User.objects.filter(username='Jim')[0],category=Category.objects.filter(name="Undergraduate")[0],highest_score=500).save()
        HighScore(user=User.objects.filter(username='Jim')[0],category=Category.objects.filter(name="Postgraduate")[0],highest_score=20).save()
        HighScore(user=User.objects.filter(username='Jane')[0],category=Category.objects.filter(name="Research")[0],highest_score=800).save()
        HighScore(user=User.objects.filter(username='Jake')[0],category=Category.objects.filter(name="Undergraduate")[0],highest_score=700).save()





def main():
    populate = Populate()
    populate.players()
    populate.categories()
    populate.levels(10,1000)
    populate.achievements()
    populate.highscores()




if __name__ == '__main__':
    main()
