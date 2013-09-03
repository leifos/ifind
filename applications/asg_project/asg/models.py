from django.db import models
from django.contrib.auth.models import User
import os
import sys
from django_countries import CountryField
from registration.signals import *
# Create your models here.

sys.path.append(os.getcwd())
from configuration import UPLOAD_DIR

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    level = models.IntegerField(default=0,blank=True)
    rating = models.IntegerField(default=0,blank=True)
    last_time_played = models.DateTimeField(null=True, blank=True)
    no_games_played = models.IntegerField(default=0,blank=True)
    total_points = models.IntegerField(default=0,blank=True)
    total_tokens = models.IntegerField(default=0,blank=True)
    no_queries_issued = models.IntegerField(default=0,blank=True)
    no_docs_assessed = models.IntegerField(default=0,blank=True)

    def __unicode__(self):
        return self.user.username


class GameExperiment(models.Model):
    name = models.CharField(max_length=128)
    config = models.IntegerField(default=0, unique=True)
    icon = models.ImageField(null=True, upload_to=UPLOAD_DIR, blank=True)
    desc = models.TextField(null=True, blank=True)
    level = models.IntegerField(default=0, blank=True)
    times_played = models.IntegerField(default=0, blank=True)
    no_queries_issued = models.IntegerField(default=0,blank=True)
    no_docs_assessed = models.IntegerField(default=0,blank=True)
    total_points = models.IntegerField(default=0,blank=True)
    total_tokens = models.IntegerField(default=0,blank=True)
    best_so_far  = models.IntegerField(default=0,blank=True)
    bronze = models.IntegerField(default=10,blank=True)
    silver = models.IntegerField(default=20,blank=True)
    gold  = models.IntegerField(default=30,blank=True)

    def __unicode__(self):
        return self.name


class MaxHighScore(models.Model):
    user = models.ForeignKey(User)
    game_experiment = models.ForeignKey(GameExperiment, null=True)
    points = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0,blank=True)
    total_tokens = models.IntegerField(default=0,blank=True)
    times_played = models.IntegerField(default=0, blank=True)

    def __unicode__(self):
        return '{0} {1} : {2}'.format(self.user.username, self.game_experiment.name, self.points)


#Need to signal to create a UserProfile when registering a User
def createUserProfile(sender, user, request, **kwargs):
    UserProfile.objects.get_or_create(user=user)

user_registered.connect(createUserProfile)

