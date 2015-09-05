__author__ = 'leif'
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from treconomics.experiment_functions import get_experiment_context
from treconomics.experiment_functions import log_event
from survey.views import handle_survey
from models import AnitaPreTaskSurveyForm, AnitaPostTask0SurveyForm, AnitaPostTask1SurveyForm, \
    AnitaPostTask2SurveyForm, AnitaPostTask3SurveyForm
from models import AnitaDemographicsSurveyForm, AnitaExit1SurveyForm, AnitaExit2SurveyForm, \
    AnitaExit3SurveyForm
from models import AnitaConsentForm
from models import MickeyPostTaskSurveyForm
from treconomics.models import TaskDescription


def handle_task_and_questions_survey(request, taskid, SurveyForm, survey_name, action, template, show_topic=True):

    request.session['taskid'] = taskid
    ec = get_experiment_context(request)
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""
    uname = request.user.username
    u = User.objects.get(username=uname)

    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event=survey_name.upper() + "_SURVEY_COMPLETED", request=request)
            return redirect('next')
        else:
            print form.errors
            errors = form.errors
            survey = SurveyForm(request.POST)

    else:
        log_event(event=survey_name.upper() + "_SURVEY_STARTED", request=request)
        survey = SurveyForm()

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire
    action_url = action + taskid + '/'

    # provide link to search interface / next system
    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'formset': survey,
                    'action': action_url,
                    'errors': errors,
                    'show_topic': show_topic}
    return render(request, template, context_dict)


@login_required
def view_alt_pretask_survey(request, taskid):
    return handle_task_and_questions_survey(request, taskid, AnitaPreTaskSurveyForm, 'ANITA_PRETASK',
                                            '/treconomics/anitapretasksurvey/', 'survey/anita_pretask_survey.html')


@login_required
def view_alt_posttask0_survey(request, taskid):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask0SurveyForm, 'ANITA_POSTTASK0',
                                            '/treconomics/anitaposttask0survey/', 'survey/anita_posttask_survey.html')


@login_required
def view_alt_posttask1_survey(request, taskid):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask1SurveyForm, 'ANITA_POSTTASK1',
                                            '/treconomics/anitaposttask1survey/', 'survey/anita_posttask_survey.html')


@login_required
def view_anita_posttask2_survey(request, taskid):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask2SurveyForm, 'ANITA_POSTTASK2',
                                            '/treconomics/anitaposttask2survey/', 'survey/anita_posttask_survey.html')


@login_required
def view_alt_posttask3_survey(request, taskid):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask3SurveyForm, 'ANITA_POSTTASK3',
                                            '/treconomics/anitaposttask3survey/', 'survey/anita_posttask_survey.html')


@login_required
def view_alt_demographic_survey(request):
    name = 'demographics'
    return handle_survey(request, AnitaDemographicsSurveyForm, name, reverse(name),
                         'survey/anita_demographics_survey.html')


@login_required
def view_alt_exit1_survey(request):
    return handle_survey(request, AnitaExit1SurveyForm, 'EXIT1', '/treconomics/anitaexit1survey/',
                         'survey/anita_exit1_survey.html')


@login_required
def view_alt_exit2_survey(request):
    return handle_survey(request, AnitaExit2SurveyForm, 'EXIT2', '/treconomics/anitaexit2survey/',
                         'survey/anita_exit2_survey.html')


@login_required
def view_alt_exit3_survey(request):
    return handle_survey(request, AnitaExit3SurveyForm, 'EXIT3', '/treconomics/anitaexit3survey/',
                         'survey/anita_exit3_survey.html')


@login_required
def view_consent(request):

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    errors = ""
    uname = request.user.username
    u = User.objects.get(username=uname)
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = AnitaConsentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            log_event("CONSENT_COMPLETED", request=request)
            return redirect('next')
        else:
            print form.errors
            errors = form.errors
            survey = AnitaConsentForm(request.POST)

    else:
        log_event("CONSENT_STARTED", request=request)
        survey = AnitaConsentForm()

    # provide link to search interface / next system
    context_dict = {'participant': uname,
                    'condition': condition,
                    'formset': survey,
                    'action': '/treconomics/consent/',
                    'errors': errors}
    return render(request, 'survey/anita_consent_form.html', context_dict)

@login_required
def view_snippet_posttask(request, taskid):
    return handle_task_and_questions_survey(request, taskid, MickeyPostTaskSurveyForm, 'MICKEY_POSTTASK',
                                            '/treconomics/mickeyposttask/', 'survey/mickey_posttask_survey.html')
