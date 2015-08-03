__author__ = 'leif'

from django.db import models
from django import forms
from django.contrib.auth.models import User

SEX_CHOICES = (('N', 'Not Indicated'),
               ('M', 'Male'), ('F', 'Female'))


class UKDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1, default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_undergrad_year = models.CharField(max_length=1, default="")

    def __unicode__(self):
        return self.user.username


class USDemographicsSurvey(models.Model):
    user = models.ForeignKey(User)
    age = models.IntegerField(default=0, help_text="Please provide your age (in years).")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, help_text="Please indicate your sex.")
    education_undergrad = models.CharField(max_length=1, default="N")
    education_undergrad_major = models.CharField(max_length=100, default="")
    education_standing = models.CharField(max_length=30, default="")

    def __unicode__(self):
        return self.user.username


class NasaSystemLoad(models.Model):
    user = models.ForeignKey(User)
    nasa_mental_demand = models.IntegerField(default=0)
    nasa_physical_demand = models.IntegerField(default=0)
    nasa_temporal = models.IntegerField(default=0)
    nasa_performance = models.IntegerField(default=0)
    nasa_effort = models.IntegerField(default=0)
    nasa_frustration = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class NasaQueryLoad(NasaSystemLoad):
    def __unicode__(self):
        return self.user.username


class NasaNavigationLoad(NasaSystemLoad):
    def __unicode__(self):
        return self.user.username


class NasaAssessmentLoad(NasaSystemLoad):
    def __unicode__(self):
        return self.user.username


class NasaFactorCompare(models.Model):
    nasa_mental_physical = forms.CharField(max_length=1)
    nasa_mental_temporal = forms.CharField(max_length=1)
    nasa_mental_performance = forms.CharField(max_length=1)
    nasa_mental_effort = forms.CharField(max_length=1)
    nasa_mental_frustration = forms.CharField(max_length=1)
    nasa_physical_temporal = forms.CharField(max_length=1)
    nasa_physical_performance = forms.CharField(max_length=1)
    nasa_physical_effort = forms.CharField(max_length=1)
    nasa_physical_frustration = forms.CharField(max_length=1)
    nasa_temporal_performance = forms.CharField(max_length=1)
    nasa_temporal_effort = forms.CharField(max_length=1)
    nasa_temporal_frustration = forms.CharField(max_length=1)
    nasa_performance_effort = forms.CharField(max_length=1)
    nasa_performance_frustration = forms.CharField(max_length=1)
    nasa_effort_frustration = forms.CharField(max_length=1)


class SearchEfficacy(models.Model):
    user = models.ForeignKey(User)
    efficacy_identify_requirements = models.IntegerField(default=0)
    efficacy_develop_queries = models.IntegerField(default=0)
    efficacy_special_syntax = models.IntegerField(default=0)
    efficacy_evaluate_list = models.IntegerField(default=0)
    efficacy_many_relevant = models.IntegerField(default=0)
    efficacy_enough_results = models.IntegerField(default=0)
    efficacy_like_a_pro = models.IntegerField(default=0)
    efficacy_few_irrelevant = models.IntegerField(default=0)
    efficacy_structure_time = models.IntegerField(default=0)
    efficacy_focus_query = models.IntegerField(default=0)
    efficacy_distinguish_relevant = models.IntegerField(default=0)
    efficacy_competent_effective = models.IntegerField(default=0)
    efficacy_little_difficulty = models.IntegerField(default=0)
    efficacy_allocated_time = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class PreTaskTopicKnowledgeSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    topic_knowledge = models.IntegerField(default=0, help_text="How much do you know about this topic?")
    topic_relevance = models.IntegerField(default=0)
    topic_interest = models.IntegerField(default=0)
    topic_searched = models.IntegerField(default=0)
    topic_difficulty = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class PostTaskTopicRatingSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    relevance_difficulty = models.IntegerField(default=0)
    relevance_skill = models.IntegerField(default=0)
    relevance_system = models.IntegerField(default=0)
    relevance_success = models.IntegerField(default=0)
    relevance_number = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class ShortStressSurvey(models.Model):
    user = models.ForeignKey(User)
    stress_confident = models.IntegerField(default=0)
    stress_alert = models.IntegerField(default=0)
    stress_others = models.IntegerField(default=0)
    stress_figure = models.IntegerField(default=0)
    stress_angry = models.IntegerField(default=0)
    stress_proficient = models.IntegerField(default=0)
    stress_irritated = models.IntegerField(default=0)
    stress_grouchy = models.IntegerField(default=0)
    stress_reflecting = models.IntegerField(default=0)
    stress_concerned = models.IntegerField(default=0)
    stress_committed = models.IntegerField(default=0)
    stress_annoyed = models.IntegerField(default=0)
    stress_impatient = models.IntegerField(default=0)
    stress_self_conscious = models.IntegerField(default=0)
    stress_daydreaming = models.IntegerField(default=0)
    stress_control = models.IntegerField(default=0)
    stress_sad = models.IntegerField(default=0)
    stress_active = models.IntegerField(default=0)
    stress_motivated = models.IntegerField(default=0)
    stress_dissatisfied = models.IntegerField(default=0)
    stress_performance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username


class ConceptListingSurvey(models.Model):
    user = models.ForeignKey(User)
    task_id = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    when = models.CharField(max_length=4, default='')
    concepts = models.TextField(default=0)
    paragraph = models.TextField(default=0)

    def __unicode__(self):
        return self.user.username


class PostConceptListingSurvey(ConceptListingSurvey):
    def __unicode__(self):
        return self.user.username


class ModifiedStressSurvey(models.Model):
    user = models.ForeignKey(User)
    stress_confident = models.IntegerField(default=0)
    stress_alert = models.IntegerField(default=0)
    stress_irritated = models.IntegerField(default=0)
    stress_others = models.IntegerField(default=0)
    stress_angry = models.IntegerField(default=0)
    stress_proficient = models.IntegerField(default=0)
    stress_grouchy = models.IntegerField(default=0)
    stress_concerned = models.IntegerField(default=0)
    stress_committed = models.IntegerField(default=0)
    stress_annoyed = models.IntegerField(default=0)
    stress_impatient = models.IntegerField(default=0)
    stress_self_conscious = models.IntegerField(default=0)
    stress_control = models.IntegerField(default=0)
    stress_sad = models.IntegerField(default=0)
    stress_active = models.IntegerField(default=0)
    stress_motivated = models.IntegerField(default=0)
    stress_dissatisfied = models.IntegerField(default=0)
    stress_performance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

