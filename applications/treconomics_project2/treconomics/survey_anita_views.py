__author__ = 'leif'
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from experiment_functions import get_experiment_context
from experiment_functions import log_event

from survey_views import handle_survey
from models_anita_experiments import AnitaPreTaskSurveyForm, AnitaPostTask1SurveyForm,AnitaPostTask2SurveyForm,AnitaPostTask3SurveyForm
from models_anita_experiments import AnitaDemographicsSurveyForm, AnitaExit1SurveyForm
from models import TaskDescription



def handle_task_and_questions_survey(request, taskid, SurveyForm, survey_name, action, template, show_topic=True):

    context = RequestContext(request)
    request.session['taskid']  = taskid
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""
    uname = request.user.username
    u = User.objects.get(username=uname)

    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event=survey_name.upper() + "_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            errors = form.errors
            survey = SurveyForm(request.POST)

    else:
        log_event(event=survey_name.upper() + "_SURVEY_STARTED", request=request)
        survey = SurveyForm()


    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionarre

    action_url = action+taskid+'/'

    # provide link to search interface / next system
    return render_to_response(template, {'participant': uname, 'condition': condition, 'task': taskid, 'topic':t.topic_num, 'tasktitle': t.title, 'taskdescription': t.description, 'formset': survey, 'action': action_url, 'errors' : errors, 'show_topic': show_topic  }, context)



@login_required
def view_anita_pretask_survey( request, taskid ):
    return handle_task_and_questions_survey(request, taskid, AnitaPreTaskSurveyForm, 'ANITA_PRETASK', '/treconomics/anitapretasksurvey/', 'survey/anita_pretask_survey.html')

@login_required
def view_anita_posttask1_survey( request, taskid ):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask1SurveyForm, 'ANITA_POSTTASK1', '/treconomics/anitaposttask1survey/', 'survey/anita_posttask_survey.html')

@login_required
def view_anita_posttask2_survey( request, taskid ):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask2SurveyForm, 'ANITA_POSTTASK2', '/treconomics/anitaposttask2survey/', 'survey/anita_posttask_survey.html')

@login_required
def view_anita_posttask3_survey( request, taskid ):
    return handle_task_and_questions_survey(request, taskid, AnitaPostTask3SurveyForm, 'ANITA_POSTTASK3', '/treconomics/anitaposttask3survey/', 'survey/anita_posttask_survey.html')


@login_required
def view_anita_demographic_survey(request):
    return handle_survey(request, AnitaDemographicsSurveyForm, 'DEMOGRAPHICS', '/treconomics/anitademographicssurvey/', 'survey/anita_demographics_survey.html')

@login_required
def view_anita_exit1_survey(request):
    return handle_survey(request, AnitaExit1SurveyForm, 'EXIT1', '/treconomics/anitaexit1survey/', 'survey/anita_exit1_survey.html')
