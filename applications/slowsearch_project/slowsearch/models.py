from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


SEX_CHOICES = (('N', 'Not Indicated'),
              ('M', 'Male'), ('F', 'Female'))

YES_CHOICES = (('', 'Not Specified'),
              ('Y', 'Yes'), ('N', 'No'))

YES_NO_CHOICES = (
    ('Y', 'Yes'), ('N', 'No'))

YEAR_CHOICES = (('', 'Not Specified'),
               ('1', 'First Year'), ('2', 'Second Year'), ('3', 'Third Year'), ('4', 'Fourth Year'),
               ('5', 'Fifth Year'), ('6', 'Completed'))


class UKDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1, default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_undergrad_year = models.CharField(max_length=1, default="")

    def __unicode__(self):
        return self.user.username




