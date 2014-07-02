from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gold_digger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from game import yieldgen, mine
from gold_digger.models import UserProfile
import pickle
from django.core.urlresolvers import reverse
import random


scan_dict = {
    'Oil lamp' : 0.2,
    'Map' : 0.3 ,
    'Sonar' : 0.5,
    'Goblin' : 0.6 ,
    'Spell' : 0.8
}

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

    if request.session['mine_type'] == '':
        mine_type = request.GET['mine type']

    else:
        mine_type = request.session['mine_type']

    print user.equipment, "EQUIPMENT"
    print request.session.items()

    if not request.session['has_mine']:
        print "GOT HERE"
        gen = yieldgen.YieldGenerator
        up_boundary = 50
        down_boundary = 10
        max_gold = random.randint(down_boundary, up_boundary)
        time_remaining = request.session['time_remaining']

        if mine_type == 'constant':
            print "constant"
            request.session['mine_type'] = 'constant'
            gen = yieldgen.ConstantYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'linear':
            print "linear"
            request.session['mine_type'] = "linear"
            gen = yieldgen.LinearYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'random':
            print "random"
            request.session['mine_type'] = 'random'
            gen = yieldgen.LinearYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'quadratic':
            print "quadratic"
            request.session['mine_type'] = 'quadratic'
            gen = yieldgen.LinearYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'exponential':
            print "exponential"
            request.session['mine_type'] = 'exponential'
            gen = yieldgen.LinearYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'cubic':
            print "cubic"
            request.session['mine_type'] = 'cubic'
            gen = yieldgen.LinearYieldGenerator(depth=10, max=max_gold, min=0)

        accuracy = scan_dict[user.equipment]
        m = mine.Mine(gen, accuracy)

        blocks = m.blocks
        request.session['has_mine'] = True
        pointer = 0
        request.session['pointer'] = pointer

        # Pickling
        file_name = "pickle"
        fileobject = open(file_name, 'wb')
        pickle.dump(blocks, fileobject)
        fileobject.close()
        request.session['pickle'] = file_name

        if time_remaining < 0:
            return HttpResponseRedirect(reverse('game_over'), context)

        return render_to_response('gold_digger/game.html',
                                  {'blocks': blocks,
                                   'user': user,
                                   'pointer': pointer,
                                   'time_remaining': time_remaining},
                                  context)

    else:

        # Unpickling
        file_name = request.session['pickle']
        fileobject = open(file_name, 'r')
        blocks = pickle.load(fileobject)
        pointer = request.session['pointer']
        time_remaining = request.session['time_remaining']
        print "Blocks Length", len(blocks)

        if time_remaining < 0:
            return HttpResponseRedirect(reverse('game_over'), context)

        return render_to_response('gold_digger/game.html', {'blocks': blocks, 'user': user, 'pointer': pointer, 'time_remaining': time_remaining}, context)

@login_required
def game_choice(request):

    context = RequestContext(request)

    request.session['has_mine'] = False
    request.session['mine_type'] = ''
    request.session['time_remaining'] = 100

    user = UserProfile.objects.get(user=request.user)
    user.gold = 0
    user.save()

    return render_to_response('gold_digger/game_choice.html', {}, context)

@login_required
def dig(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    file_name = request.session['pickle']
    fileobject = open(file_name, 'r')
    blocks = pickle.load(fileobject)

    if request.session['pointer'] == len(blocks):
        request.session['has_mine'] = False
        return HttpResponseRedirect(reverse('game'))


    gold = int(request.GET['dig'])
    pos = int(request.GET['block'])
    request.session['pointer'] += 1
    request.session['time_remaining'] -= 3


    user.gold += gold
    user.save()
    blocks[pos].dug = True


    fileobject = open(file_name, 'wb')
    pickle.dump(blocks, fileobject)
    fileobject.close()
    request.session['pickle'] = file_name
    print "Time remaining", request.session['time_remaining']


    return HttpResponseRedirect(reverse('game'), context)

@login_required
def move(request):
    context = RequestContext(request)
    request.session['has_mine'] = False
    request.session['time_remaining'] -= 5
    return HttpResponseRedirect(reverse('game'), context)

@login_required
def game_over(request):
    context = RequestContext(request)
    return render_to_response('gold_digger/game_over.html', {}, context)

