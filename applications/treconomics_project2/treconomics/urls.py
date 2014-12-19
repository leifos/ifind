__author__ = 'leif'

from django.conf.urls import patterns, url
import views, search_views, survey_views, survey_anita_views

urlpatterns = patterns('',
    url(r'^$', views.view_login),
    (r'^login/$', views.view_login),
    (r'^logout/$', views.view_logout),
    (r'^next/$', views.view_next),
    (r'^startexperiment/$', views.view_start_experiment),
    (r'^preexperiment/(?P<version>[A-Z]{2})/$', views.view_pre_experiment),
    (r'^pretask/(?P<taskid>\d+)/$', views.view_pre_task),
    (r'^prepracticetask/(?P<taskid>\d+)/$', views.view_pre_practice_task),
    (r'^pretaskquestions/(?P<taskid>\d+)/$', views.view_pre_task_with_questions),
    (r'^(?P<whoosh_docid>\d+)/$', search_views.show_document),
    (r'^saved/$', search_views.show_saved_documents),
    (r'^search/$', search_views.search),
    (r'^search/(?P<taskid>\d+)/$', search_views.search),
    (r'^posttask/(?P<taskid>\d+)/$', views.view_post_task),
    (r'^postpracticetask/(?P<taskid>\d+)/$', views.view_post_practice_task),
    (r'^posttaskquestions/(?P<taskid>\d+)/$', views.view_post_task_with_questions),
    (r'^showtask/$', views.view_show_task),
    (r'^sessioncommence/$', views.view_commence_session),    
    (r'^sessioncompleted/$', views.view_session_completed),

    (r'^postexperiment/$', views.view_post_experiment),
    (r'^endexperiment/$', views.view_end_experiment),
    (r'^performance/$', search_views.view_performance),

    (r'^suggestion_selected/$', search_views.suggestion_selected),
    (r'^suggestion_hover/$', search_views.suggestion_hover),
    (r'^query_focus/$', search_views.view_log_query_focus),
    (r'^hover/$', search_views.view_log_hover),
    (r'^autocomplete/$', search_views.autocomplete_suggestion),
    (r'^docview_delay/$', search_views.docview_delay),

    (r'^reset/$', views.view_reset_test_users),
    (r'^timeout/$', views.show_timeout_message),

    (r'^demographicssurvey/(?P<country>[A-Z]{2})/$', survey_views.view_demographics_survey),
    (r'^searchefficacysurvey/$', survey_views.view_search_efficacy_survey),
    (r'^nasaloadsurvey/$', survey_views.view_nasa_load_survey),
    (r'^nasaqueryloadsurvey/$', survey_views.view_nasa_query_load_survey),
    (r'^nasanavigationloadsurvey/$', survey_views.view_nasa_navigation_load_survey),
    (r'^nasaassessmentloadsurvey/$', survey_views.view_nasa_assessment_load_survey),
    (r'^nasafactorcomparesurvey/$', survey_views.view_nasa_factor_compare_survey),
    (r'^conceptlistingsurvey/(?P<taskid>\d+)/(?P<when>[A-Z]{3})/$', survey_views.view_concept_listing_survey),
    (r'^shortstresssurvey/$', survey_views.view_short_stress_survey),
    (r'^modifiedstresssurvey/$', survey_views.view_modified_stress_survey),

    (r'^anitapretasksurvey/(?P<taskid>\d+)/$', survey_anita_views.view_anita_pretask_survey),
    (r'^anitaposttask1survey/(?P<taskid>\d+)/$', survey_anita_views.view_anita_posttask1_survey),
    (r'^anitaposttask2survey/(?P<taskid>\d+)/$', survey_anita_views.view_anita_posttask2_survey),
    (r'^anitaposttask3survey/(?P<taskid>\d+)/$', survey_anita_views.view_anita_posttask3_survey),
    (r'^anitademographicssurvey/$', survey_anita_views.view_anita_demographic_survey),
    (r'^anitaexit1survey/$', survey_anita_views.view_anita_exit1_survey),
    )