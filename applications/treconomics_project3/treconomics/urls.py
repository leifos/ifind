__author__ = 'leif'

from django.conf.urls import patterns, url, include

from . import views
from .views import PreExperimentView
from .views import PostExperimentView
from .views import TaskSpacerView
from .views import EndExperimentView
from .views import SessionCompletedView
from search import views as search_views
import views_mickey
import survey.views as survey_views


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
             url(r'^search/(?P<taskid>\d+)/$', search_views.search),
             url(r'^posttask/(?P<taskid>\d+)/$', views.post_task, name='post-task'),
             (r'^postpracticetask/(?P<taskid>\d+)/$', views.post_practice_task),
             (r'^posttaskquestions/(?P<taskid>\d+)/$', views.post_task_with_questions),
             url(r'^taskspacer/$', TaskSpacerView.as_view()),

             (r'^showtask/$', views.show_task),
             (r'^sessioncommence/$', views.commence_session),
             url(r'^sessioncompleted/$', views.session_completed, name='session-completed'),

             url(r'^postexperiment/$', PostExperimentView.as_view()),
             url(r'^endexperiment/$', EndExperimentView.as_view()),
             (r'^performance/$', search_views.view_performance),

             (r'^suggestion_selected/$', search_views.suggestion_selected),
             (r'^suggestion_hover/$', search_views.suggestion_hover),
             (r'^query_focus/$', search_views.view_log_query_focus),
             (r'^hover/$', search_views.view_log_hover),
             (r'^autocomplete/$', search_views.autocomplete_suggestion),
             # (r'^docview_delay/$', search_views.docview_delay),

             (r'^reset/$', views.reset_test_users),
             (r'^querytest/(?P<topic_num>\d+)/$', search_views.view_run_queries),
             url(r'^timeout/$', views.show_timeout_message, name='timeout'),

             # url(r'^survey/', include('survey.urls')),

             (r'^demographicssurvey/(?P<country>[A-Z]{2})/$', survey_views.view_demographics_survey),
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

             url(r'^mickeyposttask/(?P<taskid>\d+)/$', views_mickey.mickey_posttask),

             (r'^anitapretasksurvey/(?P<taskid>\d+)/$', views_mickey.view_anita_pretask_survey),
             (r'^anitaposttask0survey/(?P<taskid>\d+)/$', views_mickey.view_anita_posttask0_survey),
             (r'^anitaposttask1survey/(?P<taskid>\d+)/$', views_mickey.view_anita_posttask1_survey),
             (r'^anitaposttask2survey/(?P<taskid>\d+)/$', views_mickey.view_anita_posttask2_survey),
             (r'^anitaposttask3survey/(?P<taskid>\d+)/$', views_mickey.view_anita_posttask3_survey),
             (r'^anitademographicssurvey/$', views_mickey.view_anita_demographic_survey),
             (r'^anitaexit1survey/$', views_mickey.view_anita_exit1_survey),
             (r'^anitaexit2survey/$', views_mickey.view_anita_exit2_survey),
             (r'^anitaexit3survey/$', views_mickey.view_anita_exit3_survey),
             (r'^anitatimeinstructions/(?P<version>[A-Z]+)/$',
             views_mickey.view_anita_time_instructions),
             (r'^consent/$', views_mickey.view_anita_consent),

    )