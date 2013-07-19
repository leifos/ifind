from django.db import models
from django.contrib.auth.models import User
import imaplib
import os
import sys
from django_countries import CountryField

sys.path.append(os.getcwd())
from configuration import APP_NAME
from configuration import UPLOAD_DIR

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(default=1)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    school = models.CharField(max_length=128)
    country = CountryField()
    city = models.CharField(max_length=128)
    xp = models.IntegerField(default=0,blank=True)
    level = models.IntegerField(default=0,blank=True)
    xp_to_next_level = models.IntegerField(default=1,blank=True)
    last_time_played = models.DateTimeField(null=True, blank=True)
    no_games_played = models.IntegerField(default=0,blank=True)
    rank = models.IntegerField(default=0,blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        app_label = APP_NAME

class Category(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(null=True, upload_to=UPLOAD_DIR, blank=True)
    desc = models.TextField(null=True, blank=True)
    is_shown = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME


class HighScore(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    highest_score = models.IntegerField(default=0)
    most_no_pages_found = models.IntegerField(default=0)
    most_no_pages_found_in_a_row = models.IntegerField(default=0)

    def __unicode__(self):
        return  self.category.name

    class Meta:
        app_label = APP_NAME


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    level_of_difficulty = models.IntegerField(default=0, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    is_shown = models.BooleanField(default=True)
    url = models.URLField(null=True)
    screenshot = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    snippet = models.TextField(null=True)
    no_times_shown = models.IntegerField(default=0)
    no_times_retrieved = models.IntegerField(default=0)
    hints = models.CharField(max_length=256, null=True, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        app_label = APP_NAME

class Achievement(models.Model):
    name = models.CharField(max_length=128)
    level_of_achievement = models.IntegerField(default=0, blank=True)
    desc = models.CharField(max_length=256)
    badge_icon = models.ImageField(null=True, upload_to=UPLOAD_DIR, blank=True)
    xp_earned = models.IntegerField(default=0, blank=True)
    achievement_class = models.CharField(max_length=128)
    def __unicode__(self):
        return self.name

    class Meta:
        app_label = APP_NAME

class CurrentGame(models.Model):
    current_page = models.ForeignKey(Page)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)
    no_of_queries_issued = models.IntegerField(default=0, null=True)
    no_of_queries_issued_for_current_page = models.IntegerField(default=0, null=True)
    no_of_successful_queries_issued = models.IntegerField(default=0, null=True)
    no_rounds = models.IntegerField(default=0, null=True)
    no_rounds_completed = models.IntegerField(default=0, null=True)
    current_score = models.IntegerField(default=0, null=True)
    last_query = models.CharField(max_length=256)
    last_query_score = models.IntegerField(default=0, null=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(auto_now_add=True)
    game_type = models.IntegerField(default=0, null=True)
    page_list = models.TextField(null=True, blank=True)
    bonus = models.IntegerField(default=100)


    def __unicode__(self):
        return self.user.username + ": " + self.current_page.title + " in " + self.category.name

    class Meta:
        app_label = APP_NAME

class PlayerAchievement (models.Model):
    user = models.ForeignKey(User)
    achievement= models.ForeignKey(Achievement)
    when = models.DateTimeField(auto_now_add=True)
    level = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.user.username + " has achieved " + self.achievement.name

    class Meta:
        app_label = APP_NAME



class Level (models.Model):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.xp) + " : " + str(self.level)

    class Meta:
        app_label = APP_NAME

