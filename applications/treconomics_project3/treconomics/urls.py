from snippets import views

__author__ = 'leif'

from django.conf.urls import patterns, url

from . import views
from .views import PreExperimentView
from .views import PostExperimentView
from .views import TaskSpacerView
from .views import EndExperimentView
from .views import SessionCompletedView
from search import views as search_views
from snippets import views as snippet


urlpatterns = \
    patterns('',
             url(r'^$', views.view_login, name='home'),
             url(r'^login/$', views.view_login, name='login'),
             url(r'^logout/$', views.view_logout, name='logout'),
             url(r'^next/$', views.view_next, name='next'),
             url(r'^startexperiment/$', views.start_experiment, name='start-experiment'),
             url(r'^preexperiment/(?P<version>[A-Z]{2})/$', PreExperimentView.as_view(), name='pre-experiment'),
             url(r'^pretask/(?P<taskid>\d+)/$', views.pre_task, name='pre-task'),
             url(r'^prepracticetask/(?P<taskid>\d+)/$', views.pre_practice_task),
             url(r'^pretaskquestions/(?P<taskid>\d+)/$', views.pre_task_with_questions),
             url(r'^(?P<whoosh_docid>\d+)/$', search_views.show_document),
             url(r'^saved/$', search_views.show_saved_documents, name='saved'),
             url(r'^search/$', search_views.search, name='search'),
             url(r'^search/(?P<taskid>\d+)/$', search_views.search, name='search-task'),
             url(r'^posttask/(?P<taskid>\d+)/$', views.post_task, name='post-task'),
             url(r'^postpracticetask/(?P<taskid>\d+)/$', views.post_practice_task),
             url(r'^posttaskquestions/(?P<taskid>\d+)/$', views.post_task_with_questions),

             url(r'^showtask/$', views.show_task),
             url(r'^sessioncommence/$', views.commence_session),
             url(r'^taskspacer/$', TaskSpacerView.as_view()),
             url(r'^sessioncompleted/$', SessionCompletedView.as_view(), name='session-completed'),
             url(r'^postexperiment/$', PostExperimentView.as_view()),
             url(r'^endexperiment/$', EndExperimentView.as_view()),

             url(r'^performance/$', search_views.view_performance),
             url(r'^suggestion_selected/$', search_views.suggestion_selected),
             url(r'^suggestion_hover/$', search_views.suggestion_hover),
             url(r'^query_focus/$', search_views.view_log_query_focus),
             url(r'^hover/$', search_views.view_log_hover),
             url(r'^autocomplete/$', search_views.autocomplete_suggestion),

             url(r'^reset/$', views.reset_test_users),
             url(r'^querytest/(?P<topic_num>\d+)/$', search_views.view_run_queries),
             url(r'^timeout/$', views.show_timeout_message, name='timeout'),

             # (r'^demographicssurvey/(?P<country>[A-Z]{2})/$', survey_views.view_demographics_survey),
             # (r'^searchefficacysurvey/$', survey_views.view_search_efficacy_survey),
             # (r'^nasaloadsurvey/$', survey_views.view_nasa_load_survey),
             # (r'^nasaqueryloadsurvey/$', survey_views.view_nasa_query_load_survey),
             # (r'^nasanavigationloadsurvey/$', survey_views.view_nasa_navigation_load_survey),
             # (r'^nasaassessmentloadsurvey/$', survey_views.view_nasa_assessment_load_survey),
             # (r'^nasafactorcomparesurvey/$', survey_views.view_nasa_factor_compare_survey),
             # (r'^conceptlistingsurvey/(?P<taskid>\d+)/(?P<when>[A-Z]{3})/$',
             # survey_views.view_concept_listing_survey),
             # (r'^shortstresssurvey/$', survey_views.view_short_stress_survey),
             # (r'^modifiedstresssurvey/$', survey_views.view_modified_stress_survey),

             url(r'^mickeyposttask/(?P<taskid>\d+)/$', snippet.view_snippet_posttask),

             (r'^anitapretasksurvey/(?P<taskid>\d+)/$', snippet.view_alt_pretask_survey),
             (r'^anitaposttask0survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask0_survey),
             (r'^anitaposttask1survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask1_survey),
             (r'^anitaposttask2survey/(?P<taskid>\d+)/$', snippet.view_anita_posttask2_survey),
             (r'^anitaposttask3survey/(?P<taskid>\d+)/$', snippet.view_alt_posttask3_survey),
             url(r'^demographicssurvey/$', snippet.view_alt_demographic_survey, name='demographics'),
             (r'^anitaexit1survey/$', snippet.view_alt_exit1_survey),
             (r'^anitaexit2survey/$', snippet.view_alt_exit2_survey),
             (r'^anitaexit3survey/$', snippet.view_alt_exit3_survey),
             (r'^consent/$', snippet.view_consent),

    )