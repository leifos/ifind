__author__ = 'mickeypash'

from django.conf.urls import patterns, url
from survey import views as survey_views

urlpatterns = patterns('',
                       url(r'^demographicssurvey/(?P<country>[A-Z]{2})/$', survey_views.view_demographics_survey),
                       (r'^searchefficacysurvey/$', survey_views.view_search_efficacy_survey),
                       (r'^nasaloadsurvey/$', survey_views.view_nasa_load_survey),
                       (r'^nasaqueryloadsurvey/$', survey_views.view_nasa_query_load_survey),
                       (r'^nasanavigationloadsurvey/$', survey_views.view_nasa_navigation_load_survey),
                       (r'^nasaassessmentloadsurvey/$', survey_views.view_nasa_assessment_load_survey),
                       (r'^nasafactorcomparesurvey/$', survey_views.view_nasa_factor_compare_survey),
                       (r'^conceptlistingsurvey/(?P<taskid>\d+)/(?P<when>[A-Z]{3})/$',
                        survey_views.view_concept_listing_survey),
                       (r'^shortstresssurvey/$', survey_views.view_short_stress_survey),
                       (r'^modifiedstresssurvey/$', survey_views.view_modified_stress_survey),
                       )