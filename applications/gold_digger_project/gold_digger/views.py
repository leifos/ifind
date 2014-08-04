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
from random import shuffle
import json

locations = ['constant', 'random', 'cubic', 'exponential', 'quadratic', 'linear']


def home(request):

    context = RequestContext(request)

    try:
        current_user = UserProfile.objects.get(user=request.user)
        scan = current_user.equipment.image.url
        tool = current_user.tool.image.url
        vehicle = current_user.vehicle.image.url
        mod_scan = int(current_user.equipment.modifier*100)
        mod_tool = int(current_user.tool.modifier*100)
        modt_tool = current_user.tool.time_modifier
        mod_vehicle = current_user.vehicle.modifier
        gold = current_user.gold


        return render_to_response('gold_digger/home.html', {'current_user': current_user,
                                                            'scan': scan,
                                                            'tool': tool,
                                                            'vehicle': vehicle,
                                                            'gold': gold,
                                                            'mod_scan': mod_scan,
                                                            'mod_tool': mod_tool,
                                                            'modt_tool': modt_tool,
                                                            'mod_vehicle': mod_vehicle}, context)

    except:
        context = RequestContext(request)
        request.session['time_remaining'] = 100
        request.session['gold'] = 0
        user_form = UserForm()
        profile_form = UserProfileForm()
        return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form}, context)


def about(request):

    context = RequestContext(request)
    return render_to_response('gold_digger/about.html', context)


def tour(request):
    context = RequestContext(request)
    return render_to_response('gold_digger/tour.html', context)


def register(request):

    context = RequestContext(request)

    registered = False

    if request.method == 'POST':

        scan = ScanningEquipment.objects.get(pk=1)
        dig_eq = DiggingEquipment.objects.get(pk=1)
        vehicle = Vehicle.objects.get(pk=1)

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST) #initial={'equipment': scan.pk, 'vehicle': vehicle, 'tool': dig_eq.pk})


        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save()


            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user


            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.equipment = ScanningEquipment.objects.get(pk=1)
            profile.vehicle = Vehicle.objects.get(pk=1)
            profile.tool = DiggingEquipment.objects.get(pk=1)
            profile.save()

            registered = True

            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

        else:
            print user_form.errors, profile_form.errors

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()


    return render_to_response('gold_digger/home.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)


def user_login(request):

    context = RequestContext(request)

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:

                login(request, user)
                request.session['time_remaining'] = 100
                request.session['gold'] = 0

                return HttpResponseRedirect(reverse('home'),context)
            else:
                return HttpResponse("Your Gold Digger account is disabled.")
        else:

            print "Invalid login details: {0}, {1}".format(username, password)
            bad_details = {'bad_details': " -=: Invalid login details supplied. :=-"}
            user_form = UserForm()
            profile_form = UserProfileForm()
            return render_to_response('gold_digger/home.html', {'user_form': user_form, 'profile_form': profile_form, 'bad_details': bad_details}, context)

    else:
        current_user = UserProfile.objects.get(user=request.user)
        scan = current_user.equipment.image.url
        tool = current_user.tool.image.url
        vehicle = current_user.vehicle.image.url
        mod_scan = int(current_user.equipment.modifier)*100
        mod_tool = int(current_user.tool.modifier)*100
        modt_tool = current_user.tool.time_modifier
        mod_vehicle = current_user.vehicle.modifier

        gold = current_user.gold
        return render_to_response('gold_digger/home.html', {'current_user': current_user,
                                                            'scan': scan,
                                                            'tool': tool,
                                                            'vehicle': vehicle,
                                                            'gold': gold,
                                                            'mod_scan': mod_scan,
                                                            'mod_tool': mod_tool,
                                                            'modt_tool': modt_tool,
                                                            'mod_vehicle': mod_vehicle}, context)


@login_required
def user_logout(request):

    logout(request)

    return HttpResponseRedirect('/gold_digger/')


@login_required
def user_profile(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    mod_scan = int((user.equipment.modifier)*100)
    mod_tool = int((user.tool.modifier)*100)
    modt_tool = user.tool.time_modifier
    mod_vehicle = int((user.tool.modifier)*100)

    return render_to_response('gold_digger/profile.html', {'user': user,
                                                           'mod_scan': mod_scan,
                                                           'mod_tool': mod_tool,
                                                           'modt_tool':modt_tool,
                                                           'mod_vehicle': mod_vehicle}, context)


@login_required
def move(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    request.session['mine_type'] = random.choice(locations)

    if request.session['time_remaining'] <= 0:
        return HttpResponseRedirect(reverse('game_over'), context)

    request.session['has_mine'] = False
    print request.session['has_mine']
    request.session['time_remaining'] -= user.vehicle.modifier
    return HttpResponseRedirect(reverse('game2'), context)


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
    mine_no = request.session['mine_no']
    request.session['mine_no'] = 0
    day_gold = request.session['gold']
    total_gold = user.gold
    request.session['gold'] = 0

    return render_to_response('gold_digger/game_over.html', {'day_gold': day_gold,
                                                             'total_gold': total_gold,
                                                             'mine_no': mine_no}, context)


def leaderboards(request):
    context = RequestContext(request)
    users_avg = UserProfile.objects.order_by('-average')
    users_gold = UserProfile.objects.order_by('-all_time_max_gold')
    users_games = UserProfile.objects.order_by('-games_played')

    return render_to_response('gold_digger/leaderboards.html', {'users_avg': users_avg, 'users_gold': users_gold, 'users_games': users_games}, context)

@login_required
def game_choice2(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)

    mine_types = ['constant', 'random', 'cubic', 'exponential', 'quadratic', 'linear']

    shuffle(mine_types)
    print mine_types
    request.session['has_mine'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    request.session['mine_no'] = 0
    scan = user.equipment.image.url
    tool = user.tool.image.url
    vehicle = user.vehicle.image.url
    mod_scan = int((user.equipment.modifier)*100)
    mod_tool = int((user.tool.modifier)*100)
    modt_tool = user.tool.time_modifier
    mod_vehicle = user.vehicle.modifier

    gold = user.gold

    return render_to_response('gold_digger/game_choice2.html', {'mine_types': mine_types,
                                                                'scan': scan,
                                                                'tool': tool,
                                                                'vehicle': vehicle,
                                                                'gold': gold,
                                                                'mod_scan': mod_scan,
                                                                'mod_tool': mod_tool,
                                                                'modt_tool': modt_tool,
                                                                'mod_vehicle': mod_vehicle}, context)


@login_required
def game2(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)


    if request.session['mine_type'] == '':
        mine_type = request.GET['mine type']

    else:
        mine_type = request.session['mine_type']

    if not request.session['has_mine']:
        gen = yieldgen.YieldGenerator

        # Randomising the max amount of gold
        up_boundary = 50
        down_boundary = 40
        max_gold = random.randint(down_boundary, up_boundary)

        limits = divide(max_gold)
        pickled_limits = pickle.dumps(limits)
        request.session['limits'] = pickled_limits
        request.session['mine_no'] += 1

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
        request.session['pointer'] = 0

        print request.session['pointer'], "POINTER!"

        scaffold = [1, 2, 3]

        # Pickling
        pickled_blocks = pickle.dumps(blocks)
        request.session['pickle'] = pickled_blocks
        move_cost = user.vehicle.modifier
        dig_cost = user.tool.time_modifier
        location = request.session['location']
        pointer = request.session['pointer']
        mine_no = request.session['mine_no']
        visibility = int((user.equipment.modifier)*10)

        if time_remaining < 0:
            return HttpResponseRedirect(reverse('game_over'), context)

        return render_to_response('gold_digger/game2.html', {'blocks': blocks,
                                                             'user': user,
                                                             'time_remaining': time_remaining,
                                                             'limits': limits,
                                                             'scaffold': scaffold,
                                                             'move_cost': move_cost,
                                                             'dig_cost': dig_cost,
                                                             'location': location,
                                                             'pointer':pointer,
                                                             'mine_no': mine_no,
                                                             'visibility': visibility}, context)
    else:
         # Unpickling
          pickled_blocks = request.session['pickle']
          blocks = pickle.loads(pickled_blocks)
          pickled_limits = request.session['limits']
          limits = pickle.loads(pickled_limits)
          move_cost = user.vehicle.modifier
          dig_cost = user.tool.time_modifier
          location = request.session['location']
          time_remaining = request.session['time_remaining']
          pointer = request.session['pointer']
          mine_no = request.session['mine_no']
          visibility = int((user.equipment.modifier)*10)


          scaffold = [1, 2, 3]

          if time_remaining < 0:
              return HttpResponseRedirect(reverse('game_over'), context)

          return render_to_response('gold_digger/game2.html', {'blocks': blocks,
                                                               'user': user,
                                                               'time_remaining': time_remaining,
                                                               'limits': limits,
                                                               'scaffold': scaffold,
                                                               'move_cost':move_cost,
                                                               'dig_cost': dig_cost,
                                                               'location': location,
                                                               'pointer': pointer,
                                                               'mine_no': mine_no,
                                                               'visibility': visibility}, context)


def divide(max_gold):

    limits = []
    span = max_gold / 6
    limits.append(max_gold)
    for x in range(6):

        max_gold -= span

        limits.append(max_gold)

    print "LIMITS", limits
    return limits


@login_required
def ajaxview(request):
    user = UserProfile.objects.get(user=request.user)
    context = RequestContext(request)

    # Unpickling the blocks
    pickled_blocks = request.session['pickle']
    blocks = pickle.loads(pickled_blocks)

    # POSTED objects
    gold_dug = int(request.POST['dig'])                         # Requesting the AMOUNT OF GOLD
    pos = int(request.POST['block'])                            # Requesting the POSITION
    print gold_dug, "GOLD DUG"

    gold_extracted = int(round(gold_dug*user.tool.modifier))    # Working out the actual amount of gold

    # Updating the session values

    request.session['pointer'] += 1
    print request.session['pointer'], "POINTER!"
    request.session['time_remaining'] -= user.tool.time_modifier
    request.session['gold'] += int(round(gold_dug*user.tool.modifier))

    # Updating user values
    user.gold += gold_extracted
    user.save()

    # Updating the block values
    blocks[pos].dug = True
    blocks[pos].gold_extracted = gold_extracted

    # Pickling
    pickled_blocks = pickle.dumps(blocks)
    request.session['pickle'] = pickled_blocks

    pickled_limits = request.session['limits']
    limits = pickle.loads(pickled_limits)

    myResponse = {}

    if gold_dug > limits[0]:
            myResponse['nuggets'] = 0
    else:
        for x in range(len(limits)-1):
            if limits[x] >= gold_dug > limits[x+1]:
                print x, "limit"
                myResponse['nuggets'] = x

    if request.session['pointer'] == len(blocks):
        myResponse['nextmine'] = True

    if request.session['time_remaining'] <= 0:
        return HttpResponse(status=204)

    myResponse['totalgold'] = user.gold
    myResponse['timeremaining'] = request.session['time_remaining']
    myResponse['currentgold'] = request.session['gold']
    myResponse['goldextracted'] = gold_extracted



    return HttpResponse(json.dumps(myResponse), content_type="application/json")


@login_required
def store(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    equipment = ScanningEquipment.objects.all()
    vehicles = Vehicle.objects.all()
    tools = DiggingEquipment.objects.all()
    gold = user.gold
    scan = user.equipment.image.url
    dig = user.tool.image.url
    move = user.vehicle.image.url
    return render_to_response('gold_digger/store.html', {'equipment': equipment,
                                                         'vehicles': vehicles,
                                                         'tools': tools,
                                                         'gold': gold,
                                                         'scan': scan,
                                                         'dig': dig,
                                                         'move': move}, context)


@login_required
def ajax_buy(request):
    user = UserProfile.objects.get(user=request.user)

    print request.POST

    if 'scan' in request.POST:
        item_name = request.POST['scan']
        item = ScanningEquipment.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.equipment = item
            user.save()
            request.session['purchase'] = True

            myResponse = {}

            myResponse['image'] = item.image.url
            myResponse['gold'] = user.gold
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

        else:
            request.session['purchase'] = False
            return HttpResponse(status=204)

    if 'tool' in request.POST:
        item_name = request.POST['tool']
        item = DiggingEquipment.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.tool = item
            user.save()
            request.session['purchase'] = True

            myResponse = {}

            myResponse['image'] = item.image.url
            myResponse['gold'] = user.gold
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

        else:
            request.session['purchase'] = False
            return HttpResponse(status=204)


    if 'vehicle' in request.POST:
        item_name = request.POST['vehicle']
        item = Vehicle.objects.get(name=item_name)

        if user.gold >= item.price:
            user.gold -= item.price
            user.vehicle = item
            user.save()
            request.session['purchase'] = True

            myResponse = {}

            myResponse['image'] = item.image.url
            myResponse['gold'] = user.gold
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

        else:
            request.session['purchase'] = False
            return HttpResponse(status=204)

@login_required
def update_location(request):
    request.session['location'] = request.POST['loc']
    request.session['mine_type'] = ''
    print request.session['location']
    return HttpResponse(status=200)