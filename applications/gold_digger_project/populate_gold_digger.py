import os


def populate():

    ### SCANNING ###

    lamp = add_scanning_equipment('Oil Lamp', 0.2, 'icons/Scan/Oil Lamp.png', 1, "It won't allow you to see much but it's better than going in blind!", 20)
    map = add_scanning_equipment('Map', 0.3, 'icons/Scan/Map.png', 200, "It probably helps knowing you're not digging in the wrong place", 30)
    sonar = add_scanning_equipment('Sonar', 0.5, 'icons/Scan/Sonar.gif', 300, "Now we're cooking with gas!", 50)
    dwarf = add_scanning_equipment('Guide Dwarf', 0.6, 'icons/Scan/Guide Dwarf.png', 400, "If you're not sure, just ask the locals!", 60)
    spell = add_scanning_equipment('Spell', 0.8, 'icons/Scan/Spell.png', 500, "Magic beats science EVERY TIME", 80)

    ### DIGGING ###

    spoon  = add_digging_equipment('Spoon', 0.3, 5, 'icons/Tools/Spoon.png', 1, "What am I supposed to do with this?", 30)
    shovel = add_digging_equipment('Shovel', 0.4, 4, 'icons/Tools/Shovel_normal.png', 200, "It's a shovel", 40)
    golden_shovel = add_digging_equipment('Golden Shovel', 0.5, 3, 'icons/Tools/Shovel_golden.png', 400, "It might seem like a bad idea, but it's not REAL gold", 50)
    dynamite = add_digging_equipment('Dynamite', 0.6, 2, 'icons/Tools/Dynamite.png', 800, "KABLAMO!", 60)
    mecha = add_digging_equipment('Mecha', 0.8, 1, 'icons/Tools/Mecha.png', 1000, "Dig ALL the gold!", 80)

    ### MOVING ###

    boots = add_vehicle('Boots', 10, 'icons/Vehicle/Boots.png', 1, "Two boots is better than no boots!")
    wheelbarrow = add_vehicle('Wheelbarrow', 9, 'icons/Vehicle/Wheelbarrow.png', 200, "Well, if you start selling mussels too, you're set!")
    cart = add_vehicle('Cart', 8, 'icons/Vehicle/Cart.png', 300, "Maybe don't ride it, it doesn't have breaks")
    donkey = add_vehicle('Donkey', 7, 'icons/Vehicle/Donkey.png', 400, "Nothing like good'ol animal power to carry your gold!")
    truck = add_vehicle('Truck', 6, 'icons/Vehicle/Truck.png', 500, "They see me rollin'!")

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', spell, wheelbarrow, shovel, 30, 0, 38.5, 0, 0)
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', lamp, boots, spoon, 34, 0, 34.5, 0, 0)
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', dwarf, truck, mecha, 56, 0, 10, 0, 0)

    ### ACHIEVEMENTS ###

    #Gold
    bronze = add_achievement('Bronze Coin', 'Dig 50 Gold Nuggets', 'icons/Achievements/Bronze.png', "So you want to be a Gold Digger...continue digging and unlock more achievements!")
    silver = add_achievement('Silver Coin', 'Dig 500 Gold Nuggets', 'icons/Achievements/Silver.png', 'What is this thing, I want GOLD!')
    gold = add_achievement("Gold Coin", 'Dig 1000 Gold Nuggets', 'icons/Achievements/GoldCoin.png', "Finally!")
    bronzeing = add_achievement('Bronze Ingot', 'Dig 5000 Gold Nuggets', 'icons/Achievements/BronzeBar.png', "So they make these out of Bronze too?")
    silvering = add_achievement('Silver Ingot', 'Dig 10000 Gold Nuggets', 'icons/Achievements/SilverBar.png', "Uuhhh!")
    golding = add_achievement('Gold Ingot', 'Dig 20000 Gold Nuggets', 'icons/Achievements/GoldBar.png', "Oooooohhh Yeeeeaah!")


    #Days
    ten_days = add_achievement("Agate", "Dig for 5 days", 'icons/Achievements/Agate.png', "You've been digging for five days! That's a lot...I guess?")
    thirty_days = add_achievement("Jade", "Dig for 10 days", 'icons/Achievements/Jade.png', "Woah, you like shinies!")
    fifty_days = add_achievement("Saphire", "Dig for 15 days", 'icons/Achievements/Saphire.png', "Dude, it's becoming an addiction...")
    hundred_days = add_achievement("Ruby", "Dig for 20 days", 'icons/Achievements/Ruby.png', "I think your family might be wondering were you are, shall I just tell them 'A Mine'? ")
    strong = add_achievement("Diamond", "Dig for 50 days", 'icons/Achievements/Diamond.png', "I'm gonna go now...")

    #Mines
    mines1 = add_achievement("Bronze Medal - Mine Guide", "Dig in 50 Mines", 'icons/Achievements/BronzeM.png', "You've been through 50 mines already!")
    mines2 = add_achievement("Silver Medal - Mole", "Dig in 100 Mines", 'icons/Achievements/SilverM.png', "You know the mines better than the surface!")
    mines3 = add_achievement("Gold Medal - Into Deep", "Dig in 300 Mines", 'icons/Achievements/GoldM.png', "Surface? What's 'Surface'?")

    banana = add_achievement("Banana", 'Found the Easter Egg', 'icons/Achievements/Banana.png', "BANANA!")

    for u in UserProfile.objects.all():
        print u


def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    return u


def add_user_profile(user, picture, location, equipment, vehicle, tool, all_time_max_gold, games_played, average, mines, game_overs):
    up = UserProfile.objects.get_or_create(user=user, picture=picture, location=location,
                                           equipment=equipment, vehicle=vehicle, tool=tool,
                                           all_time_max_gold=all_time_max_gold, games_played=games_played,
                                           average=average, mines=mines, game_overs=game_overs)[0]
    return up


def add_scanning_equipment(name, modifier, image, price, description, store_val):
    eq = ScanningEquipment.objects.get_or_create(name=name, modifier=modifier, image=image, price=price, description=description, store_val=store_val)[0]
    return eq

def add_digging_equipment(name, modifier, time_modifier, image, price, description, store_val):
    deq = DiggingEquipment.objects.get_or_create(name=name, modifier=modifier, time_modifier=time_modifier, image=image, price=price, description=description, store_val=store_val)[0]
    return deq

def add_vehicle(name, modifier, image, price, description):
    vehicle = Vehicle.objects.get_or_create(name=name, modifier=modifier, image=image, price=price, description=description)[0]
    return vehicle

def add_achievement(name, condition, image, description):
    ach = Achievements.objects.get_or_create(name=name, condition=condition, image=image, description=description)

    return ach

if __name__ == '__main__':
    print "Starting Gold Digger population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_digger_project.settings')
    from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle, Achievements
    from django.contrib.auth.models import User
    populate()