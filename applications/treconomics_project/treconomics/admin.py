__author__ = 'leif'

from models import DocumentsExamined
from models import UserProfile
from models import TaskDescription, TopicQuerySuggestion
from models_experiments import DemographicsSurvey
from models_experiments import PreTaskTopicKnowledgeSurvey, PostTaskTopicRatingSurvey
from models_experiments import NasaSystemLoad, NasaQueryLoad, NasaNavigationLoad, NasaAssessmentLoad, NasaFactorCompare
from models_experiments import SearchEfficacy

from django.contrib import admin
from django import forms


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user','data','experiment', 'condition', 'rotation', 'tasks_completed','steps_completed']
    list_display = ('user','data','experiment','condition', 'rotation', 'tasks_completed','steps_completed')


class TaskDescriptionForm( forms.ModelForm ):
    description = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = TaskDescription

class TaskDescriptionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TaskDescriptionForm

class TopicQuerySuggestionForm( forms.ModelForm ):

    class Meta:
        model = TopicQuerySuggestion

class TopicQuerySuggestionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TopicQuerySuggestionForm


class PreTaskTopicKnowledgeSurveyAdmin(admin.ModelAdmin):
    #fields = ['user','task_id','topic_num']
    list_display = ['user','task_id','topic_num']

class PostTaskTopicRatingSurveyAdmin(admin.ModelAdmin):
    #fields = ['user','task_id','topic_num']
    list_display = ['user','task_id','topic_num']

class NasaLoadAdmin(admin.ModelAdmin):
    list_display = ['user', 'nasa_mental_demand', 'nasa_physical_demand','nasa_temporal', 'nasa_performance','nasa_effort','nasa_frustration'  ]


class SearchEfficacyAdmin(admin.ModelAdmin):
    list_display = ['user']

class DemographicsSurveyAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(DocumentsExamined)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TaskDescription, TaskDescriptionAdmin)
admin.site.register(TopicQuerySuggestion, TopicQuerySuggestionAdmin)
admin.site.register(DemographicsSurvey, DemographicsSurveyAdmin)
admin.site.register(PreTaskTopicKnowledgeSurvey, PreTaskTopicKnowledgeSurveyAdmin)
admin.site.register(PostTaskTopicRatingSurvey, PostTaskTopicRatingSurveyAdmin)
admin.site.register(NasaSystemLoad, NasaLoadAdmin)
admin.site.register(NasaQueryLoad, NasaLoadAdmin)
admin.site.register(NasaNavigationLoad, NasaLoadAdmin)
admin.site.register(NasaAssessmentLoad, NasaLoadAdmin)
admin.site.register(NasaFactorCompare)
admin.site.register(SearchEfficacy, SearchEfficacyAdmin)