from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from slowsearch.forms import UserForm, UKDemographicsSurveyForm, RegValidation, FinalQuestionnaireForm
from slowsearch.models import User, UKDemographicsSurvey, Experience
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from utils import run_query


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('slowsearch/index.html', context_dict, context)


def profile(request, username):
    # Get the context from the request.
    context = RequestContext(request)

    user_name = request.user

    demographics = UKDemographicsSurvey.objects.get(user=user_name)

    # Create a context dictionary which we can pass to the template rendering engine.
    context_dict = {'user_name': user_name, 'demographics': demographics}

    return render_to_response('slowsearch/profile.html', context_dict, context)


def about(request):
     # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('slowsearch/about.html', context_dict, context)


def results(request):
     # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('slowsearch/results.html', context_dict, context)


def endexperiment(request):
     # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response('slowsearch/endexperiment.html', context_dict, context)


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

        # If the two forms are valid...
        if user_form.is_valid() and demog_form.is_valid() and validation_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            demog = demog_form.save(commit=False)
            demog.user = user

            demog.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, demog_form.errors, validation_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        demog_form = UKDemographicsSurveyForm()
        validation_form = RegValidation()

    # Render the template depending on the context.
    return render_to_response(
            'slowsearch/register.html',
            {'user_form': user_form, 'demog_form': demog_form, 'validation_form': validation_form,
             'registered': registered},
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


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/slowsearch/')


# perform a basic search using the query entered by the user
def search(request):
    context = RequestContext(request)
    result_list = []
    root_url = 'https://api.datamarket.azure.com/Bing/Search/'

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render_to_response('slowsearch/results.html', {'result_list': result_list}, context)


