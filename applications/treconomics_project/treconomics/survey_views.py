__author__ = 'leif'

# Can access them all methods but they need to be prefaced with os or datetime for example
import os
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from experiment_functions import get_experiment_context
from experiment_functions import log_event


from models_experiments import DemographicsSurvey, DemographicsSurveyForm
from models_experiments import PreTaskTopicKnowledgeSurvey, PreTaskTopicKnowledgeSurveyForm
from models_experiments import PostTaskTopicRatingSurvey, PostTaskTopicRatingSurveyForm
from models_experiments import NasaSystemLoad, NasaSystemLoadForm
from models_experiments import NasaQueryLoad, NasaQueryLoadForm
from models_experiments import NasaNavigationLoad, NasaNavigationLoadForm
from models_experiments import NasaAssessmentLoad, NasaAssessmentLoadForm
from models_experiments import NasaFactorCompare, NasaFactorCompareForm
from models_experiments import SearchEfficacy, SearchEfficacyForm
from models_experiments import ConceptListingSurvey, ConceptListingSurveyForm
from models_experiments import ShortStressSurvey, ShortStressSurveyForm
from models import TaskDescription

def handle_survey(request, SurveyForm, survey_name, action, template):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username = uname)
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event= survey_name.upper() + "_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = SurveyForm(request.POST)
    else:
        log_event(event=survey_name.upper() + "_SURVEY_STARTED", request=request)
        survey = SurveyForm()

    return render_to_response(template, {'participant': uname, 'condition': condition, 'formset': survey, 'action': action}, context)


@login_required
def view_search_efficacy_survey( request ):
    return handle_survey(request, SearchEfficacyForm, 'SELF_SEARCH_EFFICACY', '/treconomics/searchefficacysurvey/', 'survey/search_efficacy_survey.html')

@login_required
def view_demographics_survey( request ):
    return handle_survey(request, DemographicsSurveyForm, 'DEMOGRAPHICS', '/treconomics/demographicssurvey/', 'survey/demographics_survey.html')

@login_required
def view_nasa_load_survey( request ):
    return handle_survey(request, NasaSystemLoadForm, 'NASA_LOAD', '/treconomics/nasaloadsurvey/', 'survey/nasa_load_survey.html')

@login_required
def view_nasa_query_load_survey( request ):
    return handle_survey(request, NasaQueryLoadForm, 'NASA_QUERY_LOAD', '/treconomics/nasaqueryloadsurvey/', 'survey/nasa_query_load_survey.html')

@login_required
def view_nasa_navigation_load_survey( request ):
    return handle_survey(request, NasaNavigationLoadForm, 'NASA_NAVIGATION_LOAD', '/treconomics/nasanavigationloadsurvey/', 'survey/nasa_navigation_load_survey.html')

@login_required
def view_nasa_assessment_load_survey( request ):
    return handle_survey(request, NasaAssessmentLoadForm, 'NASA_ASSESSMENT_LOAD', '/treconomics/nasaassessmentloadsurvey/', 'survey/nasa_assessment_load_survey.html')

@login_required
def view_nasa_factor_compare_survey( request ):
    return handle_survey(request, NasaFactorCompareForm, 'NASA_COMPARE_FACTORS', '/treconomics/nasafactorcomparesurvey/', 'survey/nasa_factor_compare_survey.html')

@login_required
def view_short_stress_survey( request ):
    return handle_survey(request, ShortStressSurveyForm, 'SHORT_STRESS', '/treconomics/shortstresssurvey/', 'survey/short_stress_survey.html')


@login_required
def view_concept_listing_survey( request ):
    return handle_survey(request, ShortStressSurveyForm, 'CONCEPT_LISTING', '/treconomics/conceptssurvey/', 'survey/concept_listing_survey.html')


@login_required
def view_concept_listing_survey(request, taskid):
    context = RequestContext(request)
    # Set the tasks id manually from request
    request.session['taskid']  = taskid
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get( topic_num = topicnum )
    errors = ""

    uname = request.user.username
    u = User.objects.get( username = uname)

    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = ConceptListingSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="CONCEPT_LISTING_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            errors = form.errors
            survey = ConceptListingSurveyForm(request.POST)

    else:
        survey = ConceptListingSurveyForm()


    action = '/treconomics/conceptlistingsurvey/'+taskid+'/'

    # provide link to search interface / next system
    return render_to_response('survey/concept_listing_survey.html', {'participant': uname, 'condition': condition, 'task': taskid, 'topic':t.topic_num, 'tasktitle': t.title, 'taskdescription': t.description, 'formset': survey, 'action': action, 'errors' : errors  }, context)
