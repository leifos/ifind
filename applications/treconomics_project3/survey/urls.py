__author__ = 'mickeypash'

from django.conf.urls import patterns, url
from survey import views

urlpatterns = patterns('',
                       url(r'^demographicssurvey/(?P<country>[A-Z]{2})/$', views.view_demographics_survey),
                       (r'^searchefficacysurvey/$', views.view_search_efficacy_survey),
                       (r'^nasaloadsurvey/$', views.view_nasa_load_survey),
                       (r'^nasaqueryloadsurvey/$', views.view_nasa_query_load_survey),
                       (r'^nasanavigationloadsurvey/$', views.view_nasa_navigation_load_survey),
                       (r'^nasaassessmentloadsurvey/$', views.view_nasa_assessment_load_survey),
                       (r'^nasafactorcomparesurvey/$', views.view_nasa_factor_compare_survey),
                       (r'^conceptlistingsurvey/(?P<taskid>\d+)/(?P<when>[A-Z]{3})/$',
                        views.view_concept_listing_survey),
                       (r'^shortstresssurvey/$', views.view_short_stress_survey),
                       (r'^modifiedstresssurvey/$', views.view_modified_stress_survey),
)