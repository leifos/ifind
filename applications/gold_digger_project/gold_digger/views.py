from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from gold_digger.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from game import yieldgen, mine
from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle, UserAchievements, Achievements
import pickle
from django.core.urlresolvers import reverse
import random
from random import shuffle
import json

locations = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

from logger import event_logger



def home(request):

    context = RequestContext(request)

    try:
        print "Login Home"
        current_user = UserProfile.objects.get(user=request.user)
        scan = current_user.equipment.image.url
        tool = current_user.tool.image.url
        vehicle = current_user.vehicle.image.url
        mod_scan = int(current_user.equipment.modifier*100)
        mod_tool = int(current_user.tool.modifier*100)
        modt_tool = current_user.tool.time_modifier
        mod_vehicle = current_user.vehicle.modifier
        gold = current_user.gold
        request.session['days'] = current_user.games_played


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
        print "Simple Home"
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
                    print "User logged in"
                    login(request, user)

        else:
            print user_form.errors, profile_form.errors
            return render_to_response('gold_digger/home.html',
                              {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}, context)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    request.session['days'] = 1
    request.session['mine_no'] = 0
    return HttpResponseRedirect(reverse('game_choice2'), context)


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
                request.session['mine_no'] = 0
                request.session['days'] = 1

                event_logger.info('USER ' + username + ' LOGIN')

                return HttpResponseRedirect(reverse('game_choice2'), context)
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
    mod_scan_l = int(user.equipment.modifier*10)
    mod_scan = int(user.equipment.modifier*100)
    mod_tool = int(user.tool.modifier*100)
    modt_tool = user.tool.time_modifier
    achieve = UserAchievements.objects.filter(user=user)

    return render_to_response('gold_digger/profile.html', {'user': user,
                                                           'mod_scan': mod_scan,
                                                           'mod_tool': mod_tool,
                                                           'modt_tool': modt_tool,
                                                           'mod_scan_l': mod_scan_l,
                                                           'achievements': achieve}, context)


@login_required
def move(request):

    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    point_s = str(request.session['pointer'] - 1)

    if request.session['time_remaining'] <= 0:
        return HttpResponseRedirect(reverse('game_over'), context)

    request.session['has_mine'] = False
    print request.session['has_mine']
    request.session['time_remaining'] -= user.vehicle.modifier
    user.mines += 1
    user.save()

    days_s = str(request.session['days'])
    mines_s = str(user.mines)
    life_s = str(user.game_overs)
    mine_no_s = str(request.session['mine_no'])
    gold_s = str(user.gold)
    curr_s = str(request.session['gold'])
    event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' DAY ' + days_s + ' MNO ' + mine_no_s + ' TG ' + gold_s + ' CG ' + curr_s + ' MOVE ' + point_s)
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

    # Updating user values
    user.gold += request.session['gold']
    # user.mines += 1
    user.games_played += 1
    request.session['days'] += 1
    user.all_time_gold += request.session['gold']
    user.average = user.all_time_gold/user.mines
    user.save()
    request.session['has_mine'] = False
    request.session['mine_type'] = ''
    request.session['time_remaining'] = 100
    mine_no = (request.session['mine_no'])-1
    request.session['mine_no'] = 0
    day_gold = request.session['gold']
    total_gold = user.gold
    request.session['gold'] = 0
    cost = determine_cost(request.session['location'])

    gold_s = str(request.session['gold'])
    total_gold_s = str(total_gold)
    mines_s = str(user.mines)
    life_s = str(user.game_overs)
    mine_no_s = str(request.session['mine_no'])

    event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' END ' + ' MNO ' + mine_no_s + ' CG ' + gold_s + ' TG ' + total_gold_s)

    if user.gold < 40:
        return HttpResponseRedirect(reverse('game_over2'), context)

    return render_to_response('gold_digger/game_over.html', {'day_gold': day_gold,
                                                             'total_gold': total_gold,
                                                             'mine_no': mine_no,
                                                             'cost': cost}, context)


def leaderboards(request):
    context = RequestContext(request)
    users_avg = UserProfile.objects.order_by('-average')
    users_gold = UserProfile.objects.order_by('-all_time_max_gold')
    users_games = UserProfile.objects.order_by('-games_played')
    users_all_time_gold = UserProfile.objects.order_by('-all_time_gold')
    users_achievements = UserProfile.objects.all()
    achiev = UserAchievements.objects.all()

    return render_to_response('gold_digger/leaderboards.html', {'users_avg': users_avg,
                                                                'users_gold': users_gold,
                                                                'users_games': users_games,
                                                                'users_all_time_gold': users_all_time_gold,
                                                                'users_achievements': users_achievements,
                                                                'achiev': achiev}, context)

@login_required
def game_choice2(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)


    if user.gold < 40:
        return HttpResponseRedirect(reverse('game_over2'), request)

    mine_types = ['California', 'Yukon', 'Brazil', 'South Africa', 'Scotland', 'Victoria']

    request.session['has_mine'] = False
    request.session['mine_type'] = ''
    request.session['purchase'] = False
    request.session['time_remaining'] = 100
    request.session['gold'] = 0
    scan = user.equipment.image.url
    tool = user.tool.image.url
    vehicle = user.vehicle.image.url
    mod_scan = int(user.equipment.modifier*100)
    mod_tool = int(user.tool.modifier*100)
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
    days_s = str(request.session['days'])


    if request.session['mine_type'] == '':
        mine_type = request.session['location']
        user.gold -= determine_cost(mine_type)
        user.save()

        mines_s = str(user.mines)
        life_s = str(user.game_overs)
        event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' DAY ' + days_s + ' NLOC ' + mine_type + ' SCAN ' + user.equipment.name + ' DIG ' + user.tool.name + ' VEHICLE ' + user.vehicle.name)

    else:
        mine_type = request.session['mine_type']
        mine_no_s = str(request.session['mine_no'])
        mines_s = str(user.mines)
        life_s = str(user.game_overs)

        event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' DAY ' + days_s + ' LOC ' + mine_type + ' MNO ' + mine_no_s)

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

        if mine_type == 'California':
            print "California"
            request.session['mine_type'] = 'California'
            gen = yieldgen.CaliforniaQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'Yukon':
            print "Yukon"
            request.session['mine_type'] = "Yukon"
            gen = yieldgen.YukonQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'Brazil':
            print "Brazil"
            request.session['mine_type'] = 'Brazil'
            gen = yieldgen.BrazilQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'South Africa':
            print "South Africaaaaaaaaaaaaaaaaaaaaaaaa"
            request.session['mine_type'] = 'South Africa'
            gen = yieldgen.SouthAfricaQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'Scotland':
            print "Scotland"
            request.session['mine_type'] = 'Scotland'
            gen = yieldgen.ScotlandQuadraticYieldGenerator(depth=10, max=max_gold, min=0)

        elif mine_type == 'Victoria':
            print "Victoria"
            request.session['mine_type'] = 'Victoria'

            gen = yieldgen.VictoriaQuadraticYieldGenerator(depth=10, max=max_gold, min=0)
        else:
            print "Faaaaaiiilllll"
        accuracy = user.equipment.modifier
        m = mine.Mine(gen, accuracy, user)
        blocks = m.blocks

        real_array = []

        for b in blocks:
            a = round(b.gold*user.tool.modifier)
            real_array.append(a)


        real_array_s = str(real_array)
        mine_no_s = str(request.session['mine_no'])

        event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' MNO ' + mine_no_s + ' RMY ' + real_array_s)

        digcost = user.tool.time_modifier
        move_cost = user.vehicle.modifier
        digcost_s = str(digcost)
        move_cost_s = str(move_cost)
        gold_s = str(user.gold)
        should_stop_s = str(should_stop(user, real_array, digcost, move_cost))
        curr_s = str(request.session['gold'])


        event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' MNO ' + mine_no_s + ' TG ' + gold_s + ' CG ' + curr_s + ' DIGC ' + digcost_s + ' MOC ' + move_cost_s + ' SMOVE ' + should_stop_s)

        request.session['has_mine'] = True
        request.session['pointer'] = 0

        scaffold = [1, 2, 3]

        # Pickling
        pickled_blocks = pickle.dumps(blocks)
        request.session['pickle'] = pickled_blocks
        move_cost = user.vehicle.modifier
        dig_cost = user.tool.time_modifier
        location = request.session['location']
        pointer = request.session['pointer']
        mine_no = request.session['mine_no']
        visibility = int(user.equipment.modifier*10)
        mod_scan = int(user.equipment.modifier*100)
        mod_tool = int(user.tool.modifier*100)
        modt_tool = user.tool.time_modifier
        mod_vehicle = user.vehicle.modifier

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
                                                             'pointer': pointer,
                                                             'mine_no': mine_no,
                                                             'visibility': visibility,
                                                             'mod_scan': mod_scan,
                                                             'mod_tool': mod_tool,
                                                             'modt_tool': modt_tool,
                                                             'mod_vehicle': mod_vehicle}, context)
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
        visibility = int((user.equipment.modifier) * 10)
        mod_scan = int(user.equipment.modifier * 100)
        mod_tool = int(user.tool.modifier * 100)
        modt_tool = user.tool.time_modifier
        mod_vehicle = user.vehicle.modifier

        scaffold = [1, 2, 3]

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
                                                             'pointer': pointer,
                                                             'mine_no': mine_no,
                                                             'visibility': visibility,
                                                             'mod_scan': mod_scan,
                                                             'mod_tool': mod_tool,
                                                             'modt_tool': modt_tool,
                                                             'mod_vehicle': mod_vehicle}, context)


def divide(max_gold):
    limits = []
    span = max_gold / 6
    limits.append(max_gold)
    for x in range(6):

        max_gold -= span

        limits.append(max_gold)

    return limits


@login_required
def ajaxview(request):
    user = UserProfile.objects.get(user=request.user)
    context = RequestContext(request)

    # Unpickling the blocks
    pickled_blocks = request.session['pickle']
    blocks = pickle.loads(pickled_blocks)

    # POSTED objects['pointer']
    gold_dug = int(request.POST['dig'])                         # Requesting the AMOUNT OF GOLD
    gold_dug_s = str(gold_dug)
    pos = int(request.POST['block'])                            # Requesting the POSITION

    gold_extracted = int(round(gold_dug*user.tool.modifier))    # Working out the actual amount of gold
    gold_extracted_s = str(gold_extracted)
    # Updating the session values

    request.session['pointer'] += 1
    request.session['time_remaining'] -= user.tool.time_modifier
    request.session['gold'] += int(round(gold_dug*user.tool.modifier))


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
    new_id_s = user.equipment.id
    new_id_t = user.tool.id
    new_id_v = user.vehicle.id
    new_item_s = user.equipment
    new_item_t = user.tool
    new_item_v = user.vehicle

    if new_id_s != 5:
        new_id_s += 1
        new_item_s = ScanningEquipment.objects.get(id=new_id_s)

    if new_id_t != 5:
        new_id_t += 1
        new_item_t = DiggingEquipment.objects.get(id=new_id_t)

    if new_id_v != 5:
        new_id_v += 1
        new_item_v = Vehicle.objects.get(id=new_id_v)

    return render_to_response('gold_digger/store.html', {'equipment': equipment,
                                                         'vehicles': vehicles,
                                                         'tools': tools,
                                                         'gold': gold,
                                                         'scan': scan,
                                                         'dig': dig,
                                                         'move': move,
                                                         'new_item_s': new_item_s,
                                                         'new_item_t': new_item_t,
                                                         'new_item_v': new_item_v}, context)


def ajax_upgrade(request):
    user = UserProfile.objects.get(user=request.user)
    item_type = request.POST['up']
    mines_s = str(user.mines)

    if item_type == 'scan':
        item_id = user.equipment.id
        myResponse = {}
        myResponse['maxed_up'] = False
        myResponse['funds'] = False

        if item_id == 5:
            myResponse['maxed_up'] = True
            return HttpResponse(json.dumps(myResponse), content_type="application/json")
        else:
            item_id += 1
            new_item = ScanningEquipment.objects.get(id=item_id)

        if new_item.price > user.gold:
            return HttpResponse(status=204)

        if (user.gold - new_item.price) < 40:
            return HttpResponse(status=202)

        else:
            user.gold -= new_item.price
            user.equipment = new_item
            user.save()

            myResponse['image'] = new_item.image.url
            myResponse['gold'] = user.gold

            # logging
            days_s = str(request.session['days'])
            total_gold_s = str(user.gold)
            life_s = str(user.game_overs)
            mine_no_s = str(request.session['mine_no'])


            event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' MNO ' + mine_no_s + ' DAY ' + days_s + ' BUY ' + new_item.name + ' TG ' + total_gold_s)
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

    if item_type == 'tool':
        item_id = user.tool.id
        myResponse = {}
        myResponse['maxed_up'] = False
        myResponse['funds'] = False

        if item_id == 5:
            myResponse['maxed_up'] = True
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

        else:
            item_id += 1
            new_item = DiggingEquipment.objects.get(id=item_id)

        if new_item.price > user.gold:
            return HttpResponse(status=204)

        if (user.gold - new_item.price) < 40:
            return HttpResponse(status=202)


        else:
            user.gold -= new_item.price
            user.tool = new_item
            user.save()

            myResponse['image'] = new_item.image.url
            myResponse['gold'] = user.gold

            # logging
            days_s = str(request.session['days'])
            total_gold_s = str(user.gold)
            life_s = str(user.game_overs)
            mine_no_s = str(request.session['mine_no'])


            event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' MNO ' + mine_no_s + ' DAY ' + days_s + ' BUY ' + new_item.name + ' TG ' + total_gold_s)


            return HttpResponse(json.dumps(myResponse), content_type="application/json")


    if item_type == 'vehicle':
        item_id = user.vehicle.id
        myResponse = {}
        myResponse['maxed_up'] = False

        if item_id == 5:
            myResponse['maxed_up'] = True
            return HttpResponse(json.dumps(myResponse), content_type="application/json")

        else:
            item_id += 1
            new_item = Vehicle.objects.get(id=item_id)

        if new_item.price > user.gold:
            return HttpResponse(status=204)

        if (user.gold - new_item.price) < 40:
            return HttpResponse(status=202)

        else:
            user.gold -= new_item.price
            user.vehicle = new_item
            user.save()

            myResponse['image'] = new_item.image.url
            myResponse['gold'] = user.gold

            # logging
            days_s = str(request.session['days'])
            total_gold_s = str(user.gold)
            life_s = str(user.game_overs)
            mine_no_s = str(request.session['mine_no'])


            event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' MNO ' + mine_no_s + ' DAY ' + days_s + ' BUY ' + new_item.name + ' TG ' + total_gold_s)

            return HttpResponse(json.dumps(myResponse), content_type="application/json")


@login_required
def update_location(request):
    request.session['location'] = request.POST['loc']
    request.session['mine_type'] = ''
    print request.session['location']
    return HttpResponse(status=200)

@login_required
def update_cost(request):
    user = UserProfile.objects.get(user=request.user)
    user.gold -= int(request.POST['cost'])
    if user.gold < 20:
        return HttpResponse(status=204)

    user.save()

    myResponse = user.gold

    return HttpResponse(json.dumps(myResponse), content_type="application/json")


def determine_cost(mine_type):
    cost = 0
    if mine_type == 'California':
        cost = 40
    elif mine_type == 'Yukon':
        cost = 100
    elif mine_type == 'Brazil':
        cost = 200
    elif mine_type == 'South Africa':
        cost = 300
    elif mine_type == 'Scotland':
        cost = 400
    elif mine_type == 'Victoria':
        cost = 500

    return cost

@login_required
def ajax_exit(request):
    user = UserProfile.objects.get(user=request.user)
    days_s = str(request.session['days'])
    mine_no_s = str(request.session['mine_no'])
    mines_s = str(user.mines)
    life_s = str(user.game_overs)

    event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' DAY ' + days_s + ' MNO ' + mine_no_s + ' EB ' + request.POST['escape'])

    return HttpResponse(status=200)

@login_required
def game_over2(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)
    user.gold = 0
    user.equipment = ScanningEquipment.objects.get(id=1)
    user.tool = DiggingEquipment.objects.get(id=1)
    user.vehicle = Vehicle.objects.get(id=1)
    request.session['gold'] = 0
    mines = request.session['mine_no']
    request.session['mine_no'] = 0
    days = (request.session['days'])-1
    request.session['days'] = 1
    user.games_played += 1
    user.game_overs += 1
    user.gold = 100
    user.save()

    return render_to_response('gold_digger/game_over2.html', {'mines': mines,
                                                              'days': days}, context)
@login_required
def achievements(request):
    context = RequestContext(request)
    user = UserProfile.objects.get(user=request.user)

    myResponse ={}

    if user.gold < 50:
        myResponse['unlocked'] = True

    if user.gold > 50:
        achievement1 = Achievements.objects.get(id=1)
        myResponse = add_achievement(user, achievement1)

    if user.gold > 500:
        achievement2 = Achievements.objects.get(id=2)
        myResponse = add_achievement(user, achievement2)


    if user.gold > 1000:
        achievement3 = Achievements.objects.get(id=3)
        myResponse = add_achievement(user, achievement3)

    if user.gold > 5000:
        achievement3 = Achievements.objects.get(id=4)
        myResponse = add_achievement(user, achievement3)

    if user.gold > 10000:
        achievement3 = Achievements.objects.get(id=5)
        myResponse = add_achievement(user, achievement3)

    if user.gold > 20000:
        achievement3 = Achievements.objects.get(id=6)
        myResponse = add_achievement(user, achievement3)

    if user.games_played > 5:
        achievement4 = Achievements.objects.get(id=7)
        myResponse = add_achievement(user, achievement4)


    if user.games_played > 10:
        achievement5 = Achievements.objects.get(id=8)
        myResponse = add_achievement(user, achievement5)


    if user.games_played > 15:
        achievement6 = Achievements.objects.get(id=9)
        myResponse = add_achievement(user, achievement6)


    if user.games_played > 20:
        achievement7 = Achievements.objects.get(id=10)
        myResponse = add_achievement(user, achievement7)

    if  user.games_played > 50:
        achievement8 = Achievements.objects.get(id=11)
        myResponse = add_achievement(user, achievement8)


    if user.mines > 50:
        achievement9 = Achievements.objects.get(id=12)
        myResponse = add_achievement(user, achievement9)


    if user.mines > 100:
        achievement10 = Achievements.objects.get(id=13)
        myResponse = add_achievement(user, achievement10)


    if user.mines > 300:
        achievement11 = Achievements.objects.get(id=14)
        myResponse = add_achievement(user, achievement11)


    return HttpResponse(json.dumps(myResponse), content_type="application/json")



def add_achievement(user, achievement):

    myResponse = {}
    if not UserAchievements.objects.filter(user=user, achievement=achievement).exists():
        achieve = UserAchievements()
        achieve.user = user
        achieve.achievement = achievement
        achieve.save()
        print "Achievement UNLOCKED"

        myResponse['achievement_name'] = achievement.name
        myResponse['achievement_condition'] = achievement.condition
        myResponse['achievement_image'] = achievement.image.url
        myResponse['achievement_desc'] = achievement.description

        return myResponse
    else:
        myResponse['unlocked'] = True
        return myResponse

def display_achievements(request):

    ach = Achievements.objects.all()
    context = RequestContext(request)

    return render_to_response('gold_digger/achievements.html', {'achievements': ach}, context)

def egg(request):
    user = UserProfile.objects.get(user=request.user)
    achievementegg = Achievements.objects.get(id=15)

    if not UserAchievements.objects.filter(user=user, achievement=achievementegg).exists():
        achieve = UserAchievements()
        achieve.user = user
        achieve.achievement = achievementegg
        achieve.save()

        return HttpResponse(status=200)

    else:
        return HttpResponse(status=204)

def should_stop(user, real_array, digcost, movecost):
    ycmax  = 0.00
    cum_array = []
    yieldovercost = []
    cum_total = 0
    stop_here = 0

    for r in real_array:
        cum_total += r
        cum_array.append(cum_total)


    for i in range(0, len(cum_array)):
        yc = round(cum_array[i]/(movecost + ((i+1) * digcost)), 2)

        yieldovercost.append(yc)


    for i in range(0, len(yieldovercost)):

        if yieldovercost[i] >= ycmax:
            ycmax = yieldovercost[i]
            stop_here = i


    mines_s = str(user.mines)
    life_s = str(user.game_overs)
    yieldovercost_s = str(yieldovercost)

    event_logger.info('USER ' + user.user.username + ' LIFE ' + life_s + ' TOT ' + mines_s + ' YC ' + yieldovercost_s)


    return stop_here