from django.db import models
from django.contrib.auth.models import User
import imaplib
from config import UPLOAD_DIR


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    xp= models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    xp_to_next_level = models.IntegerField(default=1)
    last_time_played = models.DateTimeField()
    no_games_played = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.name


class Category(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    desc = models.TextField(null=True)
    is_shown = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Score(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    total_score = models.IntegerField(default=0)
    no_pages_found = models.IntegerField(default=0)
    no_pages_found_in_a_row = models.IntegerField(default=0)
    when = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.total_score


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    level_of_difficulty = models.IntegerField(default=0, null=True)
    desc = models.TextField(null=True)
    is_shown = models.BooleanField(default=True)
    url = models.URLField(null=True)
    screenshot = models.ImageField(null=True, upload_to=UPLOAD_DIR)
    snippet = models.TextField(null=True)
    no_times_shown = models.IntegerField(default=0, null=True)
    no_times_retrieved = models.IntegerField(default=0, null=True)
    hints = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return self.title


class Achievement(models.Model):
    name = models.CharField(max_length=128)
    level_of_achievement = models.IntegerField(default=0, null=True)
    desc = models.TextField(null=True)
    badge_icon = models.ImageField(null=True, upload_to=UPLOAD_DIR)

    def __unicode__(self):
        return self.name


class CurrentGame(models.Model):
    current_page = models.ForeignKey(Page)
    category = models.ForeignKey(Category)
    user = models.ForeignKey(User)

    no_of_queries_issued = models.IntegerField(default=0, null=True)
    no_of_successful_queries_issued = models.IntegerField(default=0, null=True)
    no_rounds = models.IntegerField(default=0, null=True)
    no_rounds_completed = models.IntegerField(default=0, null=True)
    current_score = models.IntegerField(default=0, null=True)
    last_query = models.CharField(max_length=256)
    last_query_score = models.IntegerField(default=0, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return self.user.name + ": " + self.current_page.name + " in " + self.category.name



class PlayerAchievement (models.Model):
    user = models.ForeignKey(User)
    achievement= models.ForeignKey(Achievement)
    when = models.DateTimeField()
    level = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.user.name + " has achieved " + self.achievement.name


#
class Levels (models.Model):
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.name + " has achieved " + self.achievement.name
