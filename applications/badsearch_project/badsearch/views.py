from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from forms import UserForm, UserProfileForm, DemographicsForm, ValidationForm, FinalQuestionnaireForm
from django.contrib.auth.decorators import login_required
from models import UserProfile, Demographics
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from utils import paginated_search, run_query, record_query, record_link
import datetime

def index(request):
    context = RequestContext(request)
    context_dict = {'boldmessage': "I am bold font from the context"}

    return render_to_response('badsearch/index.html', context_dict, context)

def about(request):
    context = RequestContext(request)
    return render_to_response('badsearch/about.html', {}, context)

@login_required
def profile(request):
    context = RequestContext(request)
    user = request.user
    profile = UserProfile.objects.get(user=user)
    demographics = Demographics.objects.get(user=user)

    return render_to_response('badsearch/profile.html', {'profile':profile, 'demographics':demographics}, context)

@login_required()
def final_survey(request):
    context = RequestContext(request)

    completed = False

    if request.method == 'POST':
        q_form = FinalQuestionnaireForm(data=request.POST)

        if q_form.is_valid():
            answers = q_form.save(commit=False)
            answers.user = request.user
            answers.save()

            completed = True

        else:
            print q_form.errors

    else:
        q_form = FinalQuestionnaireForm()

     # Render the template depending on the context.
    return render_to_response(
        'badsearch/finalsurvey.html', {'q_form': q_form, 'completed': completed}, context)


def endexperiment(request):
    context = RequestContext(request)
    return render_to_response('badsearch/endexperiment.html', {}, context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        validation_form = ValidationForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid() and validation_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.user_since = datetime.datetime.today()

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            user_id = user.id
            if user_id % 2 is 0:
                profile.condition=1
            elif user_id % 2 is not 0:
                profile.condition=2

            profile.save()
            registered = True
            new_user = authenticate(username=request.POST['username'],
                                    password=request.POST['password'])
            login(request, new_user)

        else:
            print user_form.errors, profile_form.errors, validation_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
        validation_form = ValidationForm()

    return render_to_response(
            'badsearch/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'validation_form': validation_form, 'registered': registered},
            context)

def demographics(request):
    context = RequestContext(request)
    completed = False
    user = request.user

    if request.method == 'POST':
        demographics_form = DemographicsForm(data=request.POST)

        if demographics_form.is_valid():
            demographics = demographics_form.save(commit=False)
            demographics.user = user

            demographics.save()

            completed = True

        else:
            print demographics_form.errors

    else:
        demographics_form = DemographicsForm

    return render_to_response('badsearch/demographics.html', {'demographics_form': demographics_form,
                                                              'completed': completed}, context)


def user_login(request):
    context = RequestContext(request)

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/badsearch/')
            else:
                return HttpResponse("Your badsearch account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render_to_response('badsearch/login.html', {}, context)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/badsearch/')

@login_required
def search(request):
    context = RequestContext(request)
    query = ""
    response = ""
    now = datetime.datetime.now().replace(tzinfo=None, microsecond=0)
    user = request.user

    record_query(user, now)

    if request.method == 'POST':
        query = request.POST['query'].strip()
        request.session['session_query'] = query
        response = paginated_search(request, query, user)

    elif request.method == 'GET':
        query = request.session['session_query']
        response = paginated_search(request, query, user)

    return render_to_response('badsearch/results.html', {'result_list': response, 'query': query}, context)

def results(request):
    context = RequestContext(request)

    return render_to_response('badsearch/results.html', context)

def goto(request, url, rank):
    user=request.user
    now = datetime.datetime.now().replace(tzinfo=None, microsecond=0)
    url_visited = url
    url_rank = rank
    record_link(user, now, url_visited, url_rank)

    return HttpResponseRedirect(url)
