from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    condition = models.IntegerField(max_length=2)
    user_since = models.DateField()
    num_query = models.IntegerField(default=0)
    num_links = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

class Demographics(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=20, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=20, default="No")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_undergrad_year = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return self.user.username

class Experience(models.Model):
    user = models.OneToOneField(User)
    ease = models.CharField(max_length=1, default="")
    boredom = models.CharField(max_length=1, default="")
    rage = models.CharField(max_length=1, default="")
    frustration = models.CharField(max_length=1, default="")
    excitement = models.CharField(max_length=1, default="")
    indifference = models.CharField(max_length=1, default="")
    confusion = models.CharField(max_length=1, default="")
    anxiety = models.CharField(max_length=1, default="")
    comment = models.CharField(max_length=200, default="")

    def __unicode__(self):
        return self.user.username


class QueryTime(models.Model):
    user = models.OneToOneField(User)
    last_query_time = models.DateTimeField()

    def __unicode__(self):
        return self.user.username

    def __get_last__(self):
        return self.last_query_time

class LinkTime(models.Model):
    user = models.OneToOneField(User)
    last_link_time = models.DateTimeField()

    def __unicode__(self):
        return self.user.username

    def __get_last__(self):
        return self.last_link_time