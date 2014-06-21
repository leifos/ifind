from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gold_digger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from game import yieldgen, mine
from gold_digger.models import UserProfile

def home(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/home.html', context)

def about(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/about.html', context)

def leaderboards(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/leaderboards.html', context)

def register(request):

    context = RequestContext(request)

    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()

            user.set_password(user.password)
            print()
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True


        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render_to_response(
            'gold_digger/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)


def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        print "AUTHENTICATED!"

        if user:
            if user.is_active:

                login(request, user)
                return HttpResponseRedirect('/gold_digger/')
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            bad_details = {'bad_details': " -=: Invalid login details supplied. :=-"}
            return render_to_response('gold_digger/home.html', bad_details, context)


    else:

        return render_to_response('gold_digger/home.html', {}, context)

@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/gold_digger/')

@login_required
def game(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    print user.equipment, "EQUIPMENT"

    if 'constant' in request.GET:
        print "constant"
        cyg = yieldgen.ConstantYieldGenerator(depth=10, max=42, min=0)
        accuracy = user.equipment
        m = mine.Mine(cyg, accuracy)
    elif 'linear' in request.GET:
        print "linear"
        lyg = yieldgen.LinearYieldGenerator(depth=10, max=42, min=0)
        accuracy = user.equipment
        m = mine.Mine(lyg, accuracy)
    elif 'random' in request.GET:
        print "random"

    elif 'quadratic' in request.GET:
        print "quadratic"

    elif 'exponential' in request.GET:
        print "exponential"

    elif 'cubic' in request.GET:
        print "cubic"




    blocks = m.blocks


    return render_to_response('gold_digger/game.html', {'blocks': blocks, 'user': user}, context)

@login_required
def game_choice(request):
    context = RequestContext(request)

    return render_to_response('gold_digger/game_choice.html', {}, context)


