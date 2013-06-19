__author__ = 'arazzouk'

from django.db import models


class User(models.Model):
    user_name = models.CharField(max_length=128)
    password = models.CharField(max_length=128)
    age = models.IntegerField(default=0, blank=True, null=True)
    gender = models.IntegerField(default=0, blank=True, null=True)
    no_games_played = models.IntegerField(default=0, null=True)
    level_of_experience = models.IntegerField(default=0, null=True)
    last_time_played = models.DateTimeField(auto_now=True)
    #ID?
    def __unicode__(self):
        return self.subject

class Score(models.Model):
    total_score = models.IntegerField(default=0, null=True)
    no_pages_found_in_a_row = models.IntegerField(default=0, null=True)
    no_pages_found= models.IntegerField(default=0, null=True)
    when = models.DateTimeField(auto_now=True)
def __unicode__(self):
    return self.subject

class Category(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(default=0, null=True)
    desc = models.CharField(max_length=1000, null=True)
    is_shown = models.BooleanField(default=True)
def __unicode__(self):
    return self.subject

class Page(models.Model):
    title = models.CharField(max_length=128)
    level_of_difficulty = models.IntegerField(default=0, blank=True, null=True)
    desc = models.CharField(max_length=1000)
    is_shown = models.BooleanField(default=True ,blank=True, null= True)
    url = models.URLField(blank=True, null=True)
    screenshot = models.ImageField(blank=True, null=True)
    snippet = models.CharField(max_length=1000)
    no_times_shown = models.IntegerField(default=0, blank=True, null=True)
    no_times_retrieved =models.IntegerField(default=0, blank=True, null=True)
    hints = models.CharField(max_length=1000)
#doc_identifier

def __unicode__(self):
    return self.subject



class Achievement(models.Model):
    name = models.CharField(max_length=128)
    level_of_achievement = models.IntegerField(default=0, blank=True, null=True)
    desc = models.CharField(max_length=1000)
    badge_icon = models.ImageField(blank=True, null=True)
#doc_identifier

def __unicode__(self):
    return self.subject


class CurrentGame(models.Model):
    name = models.CharField(max_length=128)
    no_of_queries_issued = models.IntegerField(default=0, blank=True, null=True)
    no_of_successful_queries_issued = models.IntegerField(default=0, blank=True, null=True)
    no_rounds=models.IntegerField(default=0, blank=True, null=True)
    no_rounds_completed=models.IntegerField(default=0, blank=True, null=True)
    current_score=models.IntegerField(default=0, blank=True, null=True)
    last_query=models.CharField(max_length=1000)
    last_query_score=models.IntegerField(default=0, blank=True, null=True)
    start_time=models.DateTimeField(auto_now=True)
    end_time=models.DateTimeField(auto_now=True)
    current_page = models.ForeignKey(Page)
    category=models.ForeignKey(Category)

def __unicode__(self):
    return self.subject

class PlayerAchievement (models.Model):
    when=models.DateTimeField(auto_now=True)
    level=models.IntegerField(default=0, blank=True, null=True)
    player_id = models.ForeignKey(User)
    achievement_id= models.ForeignKey(Achievements)

def __unicode__(self):
    return self.subject
