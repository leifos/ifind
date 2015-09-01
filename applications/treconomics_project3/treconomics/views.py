from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from models import DocumentsExamined
from models import TaskDescription
from survey.models import USDemographicsSurvey
from survey.models import PreTaskTopicKnowledgeSurvey
from survey.models import PostTaskTopicRatingSurvey
from survey.models import NasaSystemLoad, NasaQueryLoad, NasaNavigationLoad, NasaAssessmentLoad
from survey.models import SearchEfficacy
from survey.models import ConceptListingSurvey
from survey.models import ShortStressSurvey
from survey.forms import PreTaskTopicKnowledgeSurveyForm
from survey.forms import PostTaskTopicRatingSurveyForm
from experiment_functions import get_experiment_context, print_experiment_context
from experiment_functions import log_event
import logging

logging.basicConfig(level=logging.WARNING)
APP_NAME = '/treconomics/'


def reset_test_users(request):
    usernames = ['t1', 't2', 't3', 't4', 'a1', 'a2', 'a3', 'a4', 'd1', 'd2', 'd3', 'd4', 'd5', 'd6', 'd7', 'd8']

    for un in usernames:
        print un
        temp_user = User.objects.get(username=un)
        profile = temp_user.profile
        profile.steps_completed = 0
        profile.tasks_completed = 0
        profile.save()
        DocumentsExamined.objects.filter(user=temp_user).delete()
        PreTaskTopicKnowledgeSurvey.objects.filter(user=temp_user).delete()
        PostTaskTopicRatingSurvey.objects.filter(user=temp_user).delete()
        USDemographicsSurvey.objects.filter(user=temp_user).delete()
        USDemographicsSurvey.objects.filter(user=temp_user).delete()
        NasaSystemLoad.objects.filter(user=temp_user).delete()
        NasaQueryLoad.objects.filter(user=temp_user).delete()
        NasaNavigationLoad.objects.filter(user=temp_user).delete()
        NasaAssessmentLoad.objects.filter(user=temp_user).delete()
        SearchEfficacy.objects.filter(user=temp_user).delete()
        ShortStressSurvey.objects.filter(user=temp_user).delete()
        ConceptListingSurvey.objects.filter(user=temp_user).delete()
        request.session['current_step'] = '0'
    return HttpResponse(
        "<script type='text/javascript'>"
        "setTimeout(function(){window.location='/treconomics/'}, 1500);"
        "</script>"
        "Test users reset, redirecting to login...")


def view_login(request):
    return render(request, 'base/login.html')


def start_experiment(request):
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
                    'test': 1022,
                }

                # return HttpResponseRedirect("/treconomics/next/")
                # Instead of redirecting to next/, give back a popup launching script instead!
                return render(request, 'base/popup_launcher.html', context_dict)
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print "invalid login details " + username + " " + password
            return render(request, 'base/login.html', {'invalid': True})
    else:
        return render(request, 'base/login.html')


@login_required
def view_logout(request):
    log_event(event='EXPERIMENT_COMPLETED', request=request)
    # pid = request.user.username
    logout(request)
    # Redirect to a success page.
    return render(request, 'base/logout.html')


@login_required
def view_next(request):
    # define experiment flow here
    ec = get_experiment_context(request)
    print_experiment_context(ec)
    step = int(ec["current_step"])

    # Record the completed step
    uname = request.user.username
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.steps_completed = step
    profile.save()

    # TODO KNOWN ISSUE HERE - Clicking the back button will mean this can get out of sync.
    workflow = ec["workflow"]
    num_of_steps = len(workflow)

    # current_url = ec["current_url"]
    # find the position of the current_url in the workflow,
    # increment that position and move subject to the next step...
    # this does not solve the back button issue entirely

    if step < num_of_steps:
        next_step = step + 1
        request.session['current_step'] = str(next_step)
    else:
        next_step = step

    # Does this work correctly?
    try:
        url_to_visit_next = APP_NAME + workflow[next_step]
    except IndexError:
        url_to_visit_next = APP_NAME + workflow[next_step-1]

    print 'view_next - step : ' + str(next_step)
    print 'url to visit next: ' + str(url_to_visit_next)

    # msg = ('view_next - step : ', next_step, 'url to visit next: ', url_to_visit_next)
    # logging.debug('{0} {1} {2} {3}'.format(msg))
    # TODO request.session['current_url'] = url_to_visit_next
    return HttpResponseRedirect(url_to_visit_next)


@login_required
def pre_task(request, taskid):
    # TODO Could benefit from a generic view
    # Set the tasks id
    request.session['taskid'] = taskid

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    # provide link to search interface / next system

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description}

    return render(request, 'base/pre_task.html', context_dict)


@login_required
def pre_practice_task(request, taskid):
    # Set the tasks id
    request.session['taskid'] = taskid

    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    # provide link to search interface / next system
    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description}

    return render(request, 'base/pre_practice_task.html', context_dict)


@login_required
def post_practice_task(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.tasks_completed = int(taskid)
    profile.save()

    # write_to_log
    logging.debug('PRACTICE SEARCH TASK COMPLETED')
    log_event(event="PRACTICE_SEARCH_TASK_COMPLETED", request=request)

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    context_dict = {'participant': uname, 'condition': condition, 'task': taskid}

    return render(request, 'base/post_practice_task.html', context_dict)


@login_required
def pre_task_with_questions(request, taskid):
    # Set the tasks id manually from request
    request.session['taskid'] = taskid
    ec = get_experiment_context(request)
    # uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    t = TaskDescription.objects.get(topic_num=topicnum)
    errors = ""

    uname = request.user.username
    u = User.objects.get(username=uname)

    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = PreTaskTopicKnowledgeSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="PRE_TASK_SURVEY_COMPLETED", request=request)
            return reverse('next')
        else:
            print form.errors
            errors = form.errors
            survey = PreTaskTopicKnowledgeSurveyForm(request.POST)

    else:
        log_event(event="PRE_TASK_SURVEY_STARTED", request=request)
        survey = PreTaskTopicKnowledgeSurveyForm()

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    action = APP_NAME + 'pretaskquestions/' + taskid + '/'

    # provide link to search interface / next system

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description,
                    'formset': survey,
                    'action': action, 'errors': errors}

    return render(request, 'base/pre_task_with_questions.html', context_dict)


@login_required
def show_task(request):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    topicnum = ec["topicnum"]
    taskid = ec["taskid"]
    t = TaskDescription.objects.get(topic_num=topicnum)

    log_event(event="VIEW_TASK", request=request)

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'topic': t.topic_num,
                    'tasktitle': t.title,
                    'taskdescription': t.description}

    return render(request, 'base/show_task.html', context_dict)


@login_required
def post_task(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]

    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    profile.tasks_completed = int(taskid)
    profile.save()

    # write_to_log
    print "SEARCH TASK COMPLETED"
    log_event(event="SEARCH_TASK_COMPLETED", request=request)
    # if we had post task survey we could ask them here
    # else we can provide a link to a hosted questionnaire

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    context_dict = {'participant': uname, 'condition': condition, 'task': taskid}

    return render(request, 'base/post_task.html', context_dict)


@login_required
def post_task_with_questions(request, taskid):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    # Save out to profile what task has just been completed
    # This is probably not necessary ---- as the step  and taskid coming defines this.
    u = User.objects.get(username=uname)
    profile = u.profile
    errors = ""

    # #################
    # handle post within this element. save data to survey table,
    if request.method == 'POST':
        form = PostTaskTopicRatingSurveyForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.task_id = ec["taskid"]
            obj.topic_num = ec["topicnum"]
            obj.save()
            log_event(event="POST_TASK_SURVEY_COMPLETED", request=request)
            return redirect('next')
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
        log_event(event="POST_TASK_SURVEY_STARTED", request=request)

    # if we had a survey questions we could ask them here
    # else we can provide a link to a hosted questionnaire

    action = APP_NAME + 'posttaskquestions/' + taskid + '/'

    # if participant has completed all the tasks, go to the post experiment view
    # else direct the participant to the pre task view

    context_dict = {'participant': uname,
                    'condition': condition,
                    'task': taskid,
                    'formset': survey,
                    'action': action,
                    'errors': errors}

    return render(request, 'base/post_task_with_questions.html', context_dict)

# @login_required
# def session_completed(request):
#     ec = get_experiment_context(request)
#     uname = ec["username"]
#     condition = ec["condition"]
#     print "SESSION COMPLETED"
#     log_event(event="SESSION_COMPLETED", request=request)
#
#     context_dict = {'participant': uname, 'condition': condition}
#     return render(request, 'base/session_completed.html', context_dict)


@login_required
def commence_session(request):
    ec = get_experiment_context(request)
    uname = ec["username"]
    condition = ec["condition"]
    logging.debug('SESSION COMMENCED')
    log_event(event="SESSION_COMMENCED", request=request)

    context_dict = {'participant': uname, 'condition': condition}
    return render(request, 'base/session_commenced.html', context_dict)


@login_required
def show_timeout_message(request):
    """
    Used to display a simple page indicating the user to the fact that their time for a task has expired.
    After a 5 second delay, the page automatically redirects to /treconomics/next/.
    """
    log_event(event="EXPERIMENT_TIMEOUT", request=request)

    return render(request, 'base/timeout.html')


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class ExperimentContextMixin(LoginRequiredMixin, ContextMixin):
    """
    ExperiemntContextMixin requires LoginRequiredMixin conceptually:
    You have to be logged in for get_experiment_context to be defined!
    """
    def get_context_data(self, **kwargs):
        context = super(ExperimentContextMixin, self).get_context_data(**kwargs)

        # I'd just do this and change the templates:
        # context['experiment'] = get_experiment_context(self.request)

        # But you seem to currently want:
        ec = get_experiment_context(self.request)
        context['participant'] = ec['username']
        context['condition'] = ec['condition']

        return context


class PreExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/pre_experiment.html'


class PostExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/post_experiment.html'


class TaskSpacerView(ExperimentContextMixin, TemplateView):
    template_name = 'base/task_spacer.html'


class EndExperimentView(ExperimentContextMixin, TemplateView):
    template_name = 'base/end_experiment.html'


class SessionCompletedView(ExperimentContextMixin, TemplateView):
    template_name = 'base/session_completed.html'
    # TODO print "SESSION COMPLETED"

    def dispatch(self, request, *args, **kwargs):
        log_event(event="SESSION_COMPLETED", request=self.request)
        pass


class TimeoutView(ExperimentContextMixin, TemplateView):
    """
    Used to display a simple page indicating the user to the fact that their time for a task has expired.
    After a 5 second delay, the page automatically redirects to /treconomics/next/.
    """
    template_name = 'base/timeout.html'

    def dispatch(self, request, *args, **kwargs):
        log_event(event="EXPERIMENT_TIMEOUT", request=request)
        pass