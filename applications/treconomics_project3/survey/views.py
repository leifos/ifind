__author__ = 'leif'

# Can access them all methods but they need to be prefaced with os or datetime for example
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from treconomics.experiment_functions import get_experiment_context
from treconomics.experiment_functions import log_event
from .forms import *
from treconomics.models import TaskDescription


def handle_survey(request, SurveyForm, survey_name, action, template):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    u = User.objects.get(username=uname)
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event(event=survey_name.upper() + "_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            survey = SurveyForm(request.POST)
    else:
        log_event(event=survey_name.upper() + "_SURVEY_STARTED", request=request)
        survey = SurveyForm()

    context_dict = {'participant': uname, 'condition': condition, 'formset': survey, 'action': action}
    return render(request, template, context_dict)


@login_required
def view_search_efficacy_survey(request):
    return handle_survey(request, SearchEfficacyForm, 'SELF_SEARCH_EFFICACY', '/treconomics/searchefficacysurvey/',
                         'survey/search_efficacy_survey.html')


@login_required
def view_demographics_survey(request, country):
    if country == 'US':
        return handle_survey(request, USDemographicsSurveyForm, 'DEMOGRAPHICS', '/treconomics/demographicssurvey/US/',
                             'survey/demographics_survey.html')
    else:
        return handle_survey(request, UKDemographicsSurveyForm, 'DEMOGRAPHICS', '/treconomics/demographicssurvey/UK/',
                             'survey/demographics_survey.html')


@login_required
def view_nasa_load_survey(request):
    return handle_survey(request, NasaSystemLoadForm, 'NASA_LOAD', '/treconomics/nasaloadsurvey/',
                         'survey/nasa_load_survey.html')


@login_required
def view_nasa_query_load_survey(request):
    return handle_survey(request, NasaQueryLoadForm, 'NASA_QUERY_LOAD', '/treconomics/nasaqueryloadsurvey/',
                         'survey/nasa_query_load_survey.html')


@login_required
def view_nasa_navigation_load_survey(request):
    return handle_survey(request, NasaNavigationLoadForm, 'NASA_NAVIGATION_LOAD',
                         '/treconomics/nasanavigationloadsurvey/', 'survey/nasa_navigation_load_survey.html')


@login_required
def view_nasa_assessment_load_survey(request):
    return handle_survey(request, NasaAssessmentLoadForm, 'NASA_ASSESSMENT_LOAD',
                         '/treconomics/nasaassessmentloadsurvey/', 'survey/nasa_assessment_load_survey.html')


@login_required
def view_nasa_factor_compare_survey(request):
    return handle_survey(request, NasaFactorCompareForm, 'NASA_COMPARE_FACTORS',
                         '/treconomics/nasafactorcomparesurvey/', 'survey/nasa_factor_compare_survey.html')


@login_required
def view_short_stress_survey(request):
    return handle_survey(request, ShortStressSurveyForm, 'SHORT_STRESS', '/treconomics/shortstresssurvey/',
                         'survey/short_stress_survey.html')


@login_required
def view_modified_stress_survey(request):
    return handle_survey(request, ModifiedStressSurveyForm, 'MODIFIED_STRESS', '/treconomics/modifiedstresssurvey/',
                         'survey/short_stress_survey.html')


@login_required
def view_concept_listing_survey(request):
    return handle_survey(request, ShortStressSurveyForm, 'CONCEPT_LISTING', '/treconomics/conceptssurvey/',
                         'survey/concept_listing_survey.html')


@login_required
def view_concept_listing_survey(request, taskid, when):
    context = RequestContext(request)
    # Set the tasks id manually from request
    request.session['taskid'] = taskid
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""

    uname = request.user.username
    u = User.objects.get(username=uname)

    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = ConceptListingSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.when = when
            obj.save()
            log_event(event="CONCEPT_LISTING_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            errors = form.errors
            survey = ConceptListingSurveyForm(request.POST)

    else:
        survey = ConceptListingSurveyForm()

    action = '/treconomics/conceptlistingsurvey/' + taskid + '/' + when + '/'

    # provide link to search interface / next system
    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'formset': survey,
                    'action': action,
                    'errors': errors}

    return render(request, 'survey/concept_listing_survey.html', context_dict)
