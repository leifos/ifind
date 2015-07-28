__author__ = 'leif'

from django.contrib import admin
from django import forms

from models import DocumentsExamined
from models import UserProfile
from models import TaskDescription, TopicQuerySuggestion
from models_experiments import USDemographicsSurvey, UKDemographicsSurvey
from models_experiments import PreTaskTopicKnowledgeSurvey, PostTaskTopicRatingSurvey
from models_experiments import NasaSystemLoad, NasaQueryLoad, NasaNavigationLoad, NasaAssessmentLoad, NasaFactorCompare
from models_experiments import SearchEfficacy, ConceptListingSurvey, ShortStressSurvey, ModifiedStressSurvey
from models_anita_experiments import AnitaPreTaskSurvey, AnitaPostTask0Survey, AnitaPostTask1Survey, \
    AnitaPostTask2Survey, AnitaPostTask3Survey
from models_anita_experiments import AnitaExit1Survey, AnitaExit2Survey, AnitaExit3Survey, AnitaDemographicsSurvey


class UserProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'data', 'experiment', 'condition', 'rotation', 'tasks_completed', 'steps_completed']
    list_display = ('user', 'data', 'experiment', 'condition', 'rotation', 'tasks_completed', 'steps_completed')


class TaskDescriptionForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = TaskDescription


class TaskDescriptionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TaskDescriptionForm


class TopicQuerySuggestionForm(forms.ModelForm):
    class Meta:
        model = TopicQuerySuggestion


class TopicQuerySuggestionAdmin(admin.ModelAdmin):
    list_display = ('topic_num', 'title')
    form = TopicQuerySuggestionForm


class PreTaskTopicKnowledgeSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


class PostTaskTopicRatingSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


class NasaLoadAdmin(admin.ModelAdmin):
    list_display = ['user', 'nasa_mental_demand', 'nasa_physical_demand', 'nasa_temporal', 'nasa_performance',
                    'nasa_effort', 'nasa_frustration']


class UserSurveyAdmin(admin.ModelAdmin):
    list_display = ['user']


class TaskQuestionSurveyAdmin(admin.ModelAdmin):
    # fields = ['user','task_id','topic_num']
    list_display = ['user', 'task_id', 'topic_num']


admin.site.register(DocumentsExamined)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(TaskDescription, TaskDescriptionAdmin)
admin.site.register(TopicQuerySuggestion, TopicQuerySuggestionAdmin)
admin.site.register(USDemographicsSurvey, UserSurveyAdmin)
admin.site.register(UKDemographicsSurvey, UserSurveyAdmin)
admin.site.register(PreTaskTopicKnowledgeSurvey, PreTaskTopicKnowledgeSurveyAdmin)
admin.site.register(PostTaskTopicRatingSurvey, PostTaskTopicRatingSurveyAdmin)
admin.site.register(NasaSystemLoad, NasaLoadAdmin)
admin.site.register(NasaQueryLoad, NasaLoadAdmin)
admin.site.register(NasaNavigationLoad, NasaLoadAdmin)
admin.site.register(NasaAssessmentLoad, NasaLoadAdmin)
admin.site.register(NasaFactorCompare)
admin.site.register(SearchEfficacy, UserSurveyAdmin)
admin.site.register(ConceptListingSurvey, UserSurveyAdmin)
admin.site.register(ShortStressSurvey, UserSurveyAdmin)
admin.site.register(ModifiedStressSurvey, UserSurveyAdmin)
admin.site.register(AnitaPreTaskSurvey, TaskQuestionSurveyAdmin)
admin.site.register(AnitaPostTask0Survey, TaskQuestionSurveyAdmin)
admin.site.register(AnitaPostTask1Survey, TaskQuestionSurveyAdmin)
admin.site.register(AnitaPostTask2Survey, TaskQuestionSurveyAdmin)
admin.site.register(AnitaPostTask3Survey, TaskQuestionSurveyAdmin)
admin.site.register(AnitaExit1Survey, UserSurveyAdmin)
admin.site.register(AnitaExit2Survey, UserSurveyAdmin)
admin.site.register(AnitaExit3Survey, UserSurveyAdmin)
admin.site.register(AnitaDemographicsSurvey, UserSurveyAdmin)