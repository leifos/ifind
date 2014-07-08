from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gold_digger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from game import yieldgen, mine
from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle
import pickle
from django.core.urlresolvers import reverse
import random


# scan_dict = {
#     'Oil lamp': 0.2,
#     'Map': 0.3,
#     'Sonar': 0.5,
#     'Guide Dwarf': 0.6,
#     'Spell': 0.8
# }

def home(request):

    context = RequestContext(request)
    request.session['time_remaining'] = 100
    request.session['gold'] = 0
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

    return render_to_response('gold_digger/register.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)


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
                request.session['time_remaining'] = 100
                request.session['gold'] = 0
                request.session['order'] = 'average'
                return HttpResponseRedirect('/gold_digger/')
            else:
                return HttpResponse("Your Gold Digger account is disabled.")
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
def user_profile(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)

    return render_to_response('gold_digger/profile.html', {'user': user}, context)

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
        down_boundary = 40
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
            gen = yieldgen.RandomYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'quadratic':
            print "quadratic"
            request.session['mine_type'] = 'quadratic'
            gen = yieldgen.QuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'exponential':
            print "exponential"
            request.session['mine_type'] = 'exponential'
            gen = yieldgen.ExponentialYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'cubic':
            print "cubic"
            request.session['mine_type'] = 'cubic'
            gen = yieldgen.CubicYieldGenerator(depth=10, max=max_gold, min=0)

        accuracy = user.equipment.modifier
        m = mine.Mine(gen, accuracy)

        blocks = m.blocks
        request.session['has_mine'] = True
        pointer = 0
        request.session['pointer'] = pointer
        mine_type = request.session['mine_type']

        # Pickling
        pickled_blocks = pickle.dumps(blocks)
        request.session['pickle'] = pickled_blocks

        if time_remaining < 0:
            return HttpResponseRedirect(reverse('game_over'), context)

        return render_to_response('gold_digger/game.html', {'blocks': blocks,
                                                            'user': user,
                                                            'pointer': pointer,
                                                            'time_remaining': time_remaining,
                                                            'mine_type': mine_type}, context)
    else:

        # Unpickling
        pickled_blocks = request.session['pickle']
        blocks = pickle.loads(pickled_blocks)
        pointer = request.session['pointer']
        time_remaining = request.session['time_remaining']
        session_gold = request.session['gold']
        mine_type = request.session['mine_type']
        gold_extracted = request.session['gold_extracted']

        print "Blocks Length", len(blocks)

        if time_remaining < 0:
            return HttpResponseRedirect(reverse('game_over'), context)

        return render_to_response('gold_digger/game.html', {'blocks': blocks,
                                                            'user': user,
                                                            'pointer': pointer,
                                                            'time_remaining': time_remaining,
                                                            'gold': session_gold,
                                                            'mine_type': mine_type,
                                                            'gold_extracted': gold_extracted}, context)


@login_required
def game_choice(request):

    context = RequestContext(request)
    request.session['has_mine'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    return render_to_response('gold_digger/game_choice.html', {}, context)


@login_required
def dig(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    request.session['game_started'] = True

    pickled_blocks = request.session['pickle']
    blocks = pickle.loads(pickled_blocks)

    if request.session['pointer'] == len(blocks):
        request.session['has_mine'] = False
        return HttpResponseRedirect(reverse('game'))

    gold_dug = int(request.GET['dig'])
    gold_extracted = int(round(gold_dug*user.tool.modifier))
    pos = int(request.GET['block'])
    request.session['pointer'] += 1
    request.session['time_remaining'] -= 3

    request.session['gold'] += int(round(gold_dug*user.tool.modifier))
    user.gold += gold_extracted
    user.save()

    blocks[pos].dug = True
    blocks[pos].gold_extracted = gold_extracted

    pickled_blocks = pickle.dumps(blocks)
    request.session['pickle'] = pickled_blocks
    print "Time remaining", request.session['time_remaining']

    return HttpResponseRedirect(reverse('game'), context)


@login_required
def move(request):
    print request.GET['move']
    if request.GET['move'] == "move mine":
        context = RequestContext(request)
        request.session['has_mine'] = False
        request.session['time_remaining'] -= 5
        return HttpResponseRedirect(reverse('game'), context)

    elif request.GET['move'] == "choose mine":
        context = RequestContext(request)
        request.session['has_mine'] = False
        request.session['time_remaining'] -= 5
        return HttpResponseRedirect(reverse('gamechoice'), context)


@login_required
def back_to_main(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    request.session['has_mine'] = False
    request.session['time_remaining'] = 0
    user.gold -= request.session['gold']
    user.save()

    return HttpResponseRedirect(reverse('home'), context)


@login_required
def game_over(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)

    if user.gold > user.all_time_max_gold:
        user.all_time_max_gold = user.gold

    user.games_played += 1
    user.all_time_gold += user.gold
    user.average = user.all_time_gold/user.games_played
    user.save()
    request.session['has_mine'] = False
    request.session['time_remaining'] = 100
    return render_to_response('gold_digger/game_over.html', {}, context)


@login_required
def shop(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    equipment = ScanningEquipment.objects.all()
    vehicles = Vehicle.objects.all()
    tools = DiggingEquipment.objects.all()
    purchase = request.session['purchase']
    gold = user.gold

    print equipment
    return render_to_response('gold_digger/general_store.html', {'equipment': equipment,
                                                                 'vehicles': vehicles,
                                                                 'tools': tools,
                                                                 'purchase': purchase,
                                                                 'gold': gold
                                                                 }, context)


@login_required
def buy(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)

    print request.POST

    if 'buy equipment' in request.POST:
        item_name = request.POST['buy equipment']
        item = ScanningEquipment.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.equipment = item
            user.save()
            request.session['purchase'] = True
            print "ITEM BOUGHT"
            return HttpResponseRedirect(reverse('shop'), context)

        else:
            request.session['purchase'] = False
            return HttpResponseRedirect(reverse('shop'), context)

    if 'buy tool' in request.POST:
        item_name = request.POST['buy tool']
        item = DiggingEquipment.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.tool = item
            user.save()
            request.session['purchase'] = True
            print "ITEM BOUGHT"
            return HttpResponseRedirect(reverse('shop'), context)

        else:
            request.session['purchase'] = False
            return HttpResponseRedirect(reverse('shop'), context)

    if 'buy vehicle' in request.POST:
        item_name = request.POST['buy vehicle']
        item = Vehicle.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.vehicle = item
            user.save()
            request.session['purchase'] = True
            print "ITEM BOUGHT"
            return HttpResponseRedirect(reverse('shop'), context)

        else:
            request.session['purchase'] = False
            return HttpResponseRedirect(reverse('shop'), context)



def leaderboards(request):
    context = RequestContext(request)
    order = request.session['order']
    users = UserProfile.objects.order_by('-'+order)

    return render_to_response('gold_digger/leaderboards.html', {'users': users}, context)


@login_required
def change_order(request):
    context = RequestContext(request)
    order = request.POST['rank']
    request.session['order'] = order

    return HttpResponseRedirect(reverse('leaderboards'), context)