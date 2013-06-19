from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0, blank=True, null=True)
    gender = models.IntegerField(default=0, blank=True, null=True)
    is_native_english = models.BooleanField(default=True, blank=True, null=True)
    is_staff = models.BooleanField(default=True, blank=True, null=True)
    is_student = models.BooleanField(default=True, blanl=True, null=True)
    level_of_experience = models.IntegerField(default=0, null=True)
    last_time_played = models.DateTimeField()
    no_games_played = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.user.name


class Score(models.Model):
    user = models.ForeignKey(User)
    category = models.ForeignKey(Category)
    total_score = models.IntegerField(default=0, null=True)
    no_pages_found = models.IntegerField(default=0, null=True)
    no_pages_found_in_a_row = models.IntegerField(default=0, null=True)
    when = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.total_score


class Category(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(default=0, null=True)
    desc = models.TextField(null=True)
    is_shown = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    level_of_difficulty = models.IntegerField(default=0, null=True)
    desc = models.TextField(null=True)
    is_shown = models.BooleanField(default=True, null=True)
    url = models.URLField(null=True)
    screenshot = models.ImageField(null=True)
    snippet = models.TextField(null=True)
    no_times_shown = models.IntegerField(default=0, null=True)
    no_times_retrieved = models.IntegerField(default=0, null=True)
    hints = models.Textfield(null=True)

    def __unicode__(self):
        return self.title


class Achievement(models.Model):
    name = models.CharField(max_length=128)
    level_of_achievement = models.IntegerField(default=0, null=True)
    desc = models.TextField(null=True)
    badge_icon = models.ImageField(null=True)

    def __unicode__(self):
        return self.name


class CurrentGame(models.Model):
    current_page = models.ForeignKey(Page)
    category = models.ForeignKey(Category)
    User = models.ForeignKey(User)
    name = models.CharField(max_length=128)
    no_of_queries_issued = models.IntegerField(default=0, null=True)
    no_of_successful_queries_issued = models.IntegerField(default=0, null=True)
    no_rounds = models.IntegerField(default=0, null=True)
    no_rounds_completed = models.IntegerField(default=0, null=True)
    current_score = models.IntegerField(default=0, null=True)
    last_query = models.CharField(max_length=1000)
    last_query_score = models.IntegerField(default=0, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name


class PlayerAchievement (models.Model):
    user = models.ForeignKey(User)
    achievement= models.ForeignKey(Achievement)
    when = models.DateTimeField()
    level = models.IntegerField(default=0, null=True)

    def __unicode__(self):
        return self.user.name + " has achieved " + self.achievement.name
