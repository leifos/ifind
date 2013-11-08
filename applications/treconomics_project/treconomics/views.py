# Create your views here.
import os
import datetime
# Django
from django.template.context import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import DocumentsExamined
from models import TaskDescription
from models_experiments import DemographicsSurvey, DemographicsSurveyForm
from models_experiments import PreTaskTopicKnowledgeSurvey, PreTaskTopicKnowledgeSurveyForm
from models_experiments import PostTaskTopicRatingSurvey, PostTaskTopicRatingSurveyForm

from models_experiments import NasaSystemLoad, NasaQueryLoad, NasaNavigationLoad, NasaAssessmentLoad
from models_experiments import SearchEfficacy

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.forms.models import inlineformset_factory, modelformset_factory

from experiment_functions import get_experiment_context, print_experiment_context
from experiment_functions import log_event


def view_reset_test_users(request):
    usernames = ['t1', 't2', 't3', 't4', 'a1', 'a2', 'a3', 'a4']

    for un in usernames:
        print un
        temp_user = User.objects.get(username=un)
        profile = temp_user.get_profile()
        profile.steps_completed = 0
        profile.tasks_completed = 0
        profile.save()
        docs = DocumentsExamined.objects.filter(user=temp_user).delete()
        pre_tasks = PreTaskTopicKnowledgeSurvey.objects.filter(user=temp_user).delete()
        post_tasks = PostTaskTopicRatingSurvey.objects.filter(user=temp_user).delete()
        demo = DemographicsSurvey.objects.filter(user=temp_user).delete()
        nasa = NasaSystemLoad.objects.filter(user=temp_user).delete()
        nasaq = NasaQueryLoad.objects.filter(user=temp_user).delete()
        nasan = NasaNavigationLoad.objects.filter(user=temp_user).delete()
        nasaa = NasaAssessmentLoad.objects.filter(user=temp_user).delete()
        eff = SearchEfficacy.objects.filter(user=temp_user).delete()
        request.session['current_step'] = '0'
    return HttpResponse("Test users reset.")

def view_login(request):
    context = RequestContext(request)
    return render_to_response('base/login.html', {}, context)

def view_start_experiment(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                # set cookies for experiment
                ec = get_experiment_context(request)
                print_experiment_context(ec)

                context_dict = {
                    'popup_width': 1024,
                    'popup_height': 1024,
                }

                # return HttpResponseRedirect("/treconomics/next/")
                # Instead of redirecting to next/, give back a popup launching script instead!
                return render_to_response('base/popup_launcher.html', context_dict, context)
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print  "invalid login details " + username + " " + password
            return render_to_response('base/login.html', {}, context)
    else:
        return render_to_response('base/login.html', {}, context)


@login_required
def view_logout(request):
    context = RequestContext(request)
    pid = request.user.username
    logout(request)
    # Redirect to a success page.
    return render_to_response('base/logout.html', {}, context)

@login_required
def view_next(request):
    # define experiment flow here
    ec = get_experiment_context(request)
    print_experiment_context(ec)
    step = int(ec["current_step"])

    #Record the completed step
    uname = request.user.username
    u = User.objects.get(username=uname)
    profile = u.get_profile()
    profile.steps_completed = step
    profile.save()

    # KNOWN ISSUE HERE - Clicking the back button will mean this can get out of sync.
    workflow = ec["workflow"]
    num_of_steps = len(workflow)

    #current_url = ec["current_url"]
    # find the position of the current_url in the workflow,
    # increment that position and move subject to the next step...
    # this does not solve the back button issue entirely

    if step < num_of_steps:
        next_step = step + 1
        request.session['current_step'] = str(next_step)
    else:
        next_step = step



    url_to_visit_next = workflow[next_step]
    print "view_next - step : "+ str(next_step) + " url to vist next: " + url_to_visit_next
    #request.session['current_url'] = url_to_visit_next
    return HttpResponseRedirect( url_to_visit_next )

@login_required
def view_pre_task(request, taskid):
    context = RequestContext(request)
    # Set the tasks id
    request.session['taskid']  = taskid

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get( topic_num = topicnum )

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionarre

    # provide link to search interface / next system
    return render_to_response('base/pre_task.html', {'participant': uname, 'condition': condition, 'task': taskid, 'topic':t.topic_num, 'tasktitle': t.title, 'taskdescription': t.description }, context)


@login_required
def view_pre_task_with_questions(request, taskid):
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
        print "IN POST"
        form = PreTaskTopicKnowledgeSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="PRE_TASK_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            errors = form.errors
            survey = PreTaskTopicKnowledgeSurveyForm(request.POST)

    else:
        survey = PreTaskTopicKnowledgeSurveyForm()


    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionarre

    action = '/treconomics/pretaskquestions/'+taskid+'/'

    # provide link to search interface / next system
    return render_to_response('base/pre_task_with_questions.html', {'participant': uname, 'condition': condition, 'task': taskid, 'topic':t.topic_num, 'tasktitle': t.title, 'taskdescription': t.description, 'formset': survey, 'action': action, 'errors' : errors  }, context)


@login_required
def view_show_task(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    taskid = ec["taskid"]
    t = TaskDescription.objects.get( topic_num = topicnum )

    return render_to_response('base/show_task.html', {'participant': uname, 'condition': condition, 'task': taskid, 'topic':t.topic_num, 'tasktitle': t.title, 'taskdescription': t.description }, context)


@login_required
def view_post_task(request, taskid):
    context = RequestContext(request)

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    # Save out to profile what task has just been completed
    # This is probably not neccessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.get_profile()
    profile.tasks_completed = int(taskid)
    profile.save()

    # write_to_log
    print "SEARCH TASK COMPLETED"
    log_event(event="SEARCH_TASK_COMPLETED", request=request)
    # if we had post task survey we could ask them here
    # else we can provide a link to a hosted questionairre

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view
    return render_to_response('base/post_task.html', {'participant': uname, 'condition': condition, 'task': taskid }, context)

@login_required
def view_post_task_with_questions(request, taskid):
    context = RequestContext(request)

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    # Save out to profile what task has just been completed
    # This is probably not neccessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.get_profile()
    errors = ""

##################
    #handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = PostTaskTopicRatingSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="POST_TASK_SURVEY_COMPLETED", request=request)
            return HttpResponseRedirect('/treconomics/next/')
        else:
            print form.errors
            errors = form.errors
            survey = PostTaskTopicRatingSurveyForm(request.POST)
    else:
        survey = PostTaskTopicRatingSurveyForm()
        profile.tasks_completed = int(taskid)
        profile.save()
        print "SEARCH TASK COMPLETED"
        log_event(event="SEARCH_TASK_COMPLETED", request=request)

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionarre

    action = '/treconomics/posttaskquestions/'+taskid+'/'

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view
    return render_to_response('base/post_task_with_questions.html', {'participant': uname, 'condition': condition, 'task': taskid, 'formset': survey, 'action': action, 'errors' : errors }, context)


@login_required
def view_pre_experiment(request, version):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    if version == 'US':
        return render_to_response('base/pre_experiment_us.html', {'participant': uname, 'condition': condition }, context)
    else:
        return render_to_response('base/pre_experiment.html', {'participant': uname, 'condition': condition }, context)

@login_required
def view_post_experiment(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    # if we had post task survey we could ask them here
    # else we can provide a link to a hosted questionairre

    # Provide debreifing

    return render_to_response('base/post_experiment.html', {'participant': uname, 'condition': condition }, context)

@login_required
def view_end_experiment(request):
    context = RequestContext(request)
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    # if we had post task survey we could ask them here
    # else we can provide a link to a hosted questionairre

    # Provide debreifing
    return render_to_response('base/end_experiment.html', {'participant': uname, 'condition': condition }, context)

