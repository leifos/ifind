
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from slowsearch.forms import UserForm, UKDemographicsSurveyForm, RegValidation, FinalQuestionnaireForm, UserProfileForm
from slowsearch.models import User, UKDemographicsSurvey, Experience, QueryTime, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from utils import paginated_search, get_condition, record_query, record_link
import datetime
from datetime import timedelta
from logger_practice import event_logger


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('slowsearch/index.html', context)


@login_required()
def profile(request, *args, **kwargs):
    # Get the context from the request.
    context = RequestContext(request)

    user_name = request.user
    demographics = UKDemographicsSurvey.objects.get(user=user_name)
    profile = UserProfile.objects.get(user=user_name)

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {'user_name': user_name, 'demographics': demographics, 'profile':profile}
    return render_to_response('slowsearch/profile.html', context_dict, context)


def about(request):
    context = RequestContext(request)
    return render_to_response('slowsearch/about.html', context)


def results(request):
    context = RequestContext(request)
    return render_to_response('slowsearch/results.html', context)


def endexperiment(request):
    context = RequestContext(request)
    return render_to_response('slowsearch/endexperiment.html', context)


def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UKDemographicsSurveyForm
        user_form = UserForm(data=request.POST)
        demog_form = UKDemographicsSurveyForm(data=request.POST)
        validation_form = RegValidation(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the forms are valid...
        if user_form.is_valid() and demog_form.is_valid() and validation_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            user_profile = profile_form.save(commit=False)
            user_profile.user = user

            if user.id % 2 == 0:
                user_profile.condition = 1

            elif user.id % 2 != 0:
                user_profile.condition = 2

            user_profile.user_since = datetime.datetime.today()
            user_profile.save()

            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, user)

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, validation_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        validation_form = RegValidation()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'slowsearch/register.html',
            {'user_form': user_form, 'validation_form': validation_form,
             'profile_form': profile_form,
             'registered': registered},
            context)


def demographic(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    completed = False
    user = request.user
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        demog_form = UKDemographicsSurveyForm(data=request.POST)

        if demog_form.is_valid():
            demog = demog_form.save(commit=False)
            demog.user = user

            demog.save()

            completed = True

        else:
            print demog_form.errors

    else:
        demog_form = UKDemographicsSurveyForm

    return render_to_response('slowsearch/demographic.html', {'demog_form': demog_form, 'completed': completed},
                              context)


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
        'slowsearch/finalsurvey.html', {'q_form': q_form, 'completed': completed}, context)


def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/slowsearch/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('slowsearch/login.html', {}, context)


def user_logout(request):

    return render_to_response('/slowsearch/logged_out.html')


# perform a basic search using the query entered by the user
# logs the time spent on the results page, provided it is less than an hour
@login_required()
def search(request):
    context = RequestContext(request)
    query = ""
    contacts = ""

    user = request.user
    now = datetime.datetime.now().replace(tzinfo=None, microsecond=0)
    page = request.REQUEST.get('page')
    cnd = get_condition(request)

    u_ID = (user.id)
    str_u_ID = str(u_ID)

    record_query(user, now)

    if request.method == 'POST':
        query = request.POST['query'].strip()
        request.session['session_query'] = query
        contacts = paginated_search(query, cnd, u_ID, page, user)

    elif request.method == 'GET':
        query = request.session['session_query']
        contacts = paginated_search(query, cnd, u_ID, page, user)

    return render_to_response('slowsearch/results.html', {'contacts': contacts, 'query': query}, context)


def goto(request, url, rank):
    user = request.user
    now = datetime.datetime.now().replace(tzinfo=None, microsecond=0)
    url_visited = url
    url_rank = rank
    record_link(user, now, url_visited, url_rank)

    return HttpResponseRedirect(url)