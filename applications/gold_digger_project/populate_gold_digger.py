import os


def populate():

    ### SCANNING ###

    lamp = add_scanning_equipment('Oil Lamp', 0.2, 'icons/Scan/Oil Lamp.png', 1, "It won't allow you to see much but it's better than going in blind!", 20)
    map = add_scanning_equipment('Map', 0.3, 'icons/Scan/Map.png', 100, "It probably helps knowing you're not digging in the wrong place", 30)
    sonar = add_scanning_equipment('Sonar', 0.5, 'icons/Scan/Sonar.gif', 200, "Now we're cooking with gas!", 50)
    dwarf = add_scanning_equipment('Guide Dwarf', 0.6, 'icons/Scan/Guide Dwarf.png', 300, "If you're not sure, just ask the locals!", 60)
    spell = add_scanning_equipment('Spell', 0.8, 'icons/Scan/Spell.png', 500, "Magic beats science EVERY TIME", 80)

    ### DIGGING ###

    spoon  = add_digging_equipment('Spoon', 0.3, 10, 'icons/Tools/Spoon.png', 1, "What am I supposed to do with this?", 30)
    shovel = add_digging_equipment('Shovel', 0.4, 7, 'icons/Tools/Shovel_normal.png', 100, "It's a shovel", 40)
    golden_shovel = add_digging_equipment('Golden Shovel', 0.5, 6, 'icons/Tools/Shovel_golden.png', 200, "It might seem like a bad idea, but it's not REAL gold", 50)
    dynamite = add_digging_equipment('Dynamite', 0.6, 5, 'icons/Tools/Dynamite.png', 300, "KABLAMO!", 60)
    mecha = add_digging_equipment('Mecha', 0.8, 3, 'icons/Tools/Mecha.png', 500, "Dig ALL the gold!", 80)

    ### MOVING ###

    boots = add_vehicle('Boots', 15, 'icons/Vehicle/Boots.png', 1, "Two boots is better than no boots!")
    wheelbarrow = add_vehicle('Wheelbarrow', 10, 'icons/Vehicle/Wheelbarrow.png', 100, "Well, if you start selling mussels too, you're set!")
    cart = add_vehicle('Cart', 8, 'icons/Vehicle/Cart.png', 150, "Maybe don't ride it, it doesn't have breaks")
    donkey = add_vehicle('Donkey', 5, 'icons/Vehicle/Donkey.png', 200, "Nothing like good'ol animal power to carry your gold!")
    truck = add_vehicle('Truck', 3, 'icons/Vehicle/Truck.png', 400, "They see me rollin'!")

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', spell, wheelbarrow, shovel, 1234, 0, 308.5, 0)
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', lamp, boots, spoon, 345, 0, 34.5, 0)
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', dwarf, truck, mecha, 567, 0, 1000, 0)

    ### ACHIEVEMENTS ###

    #Gold
    bronze = add_achievement('Bronze Coin', '50 Gold Nuggets', 'icons/Achievements/Bronze.png', "So you want to be a Gold Digger...continue digging and unlock more achievements!")
    silver = add_achievement('Silver Coin', '200 Gold Nuggets', 'icons/Achievements/Silver.png', 'What is this thing, I want GOLD!')
    gold = add_achievement("Gold Coin", '500 Gold Nuggets', 'icons/Achievements/GoldCoin.png', "Finally!")

    #Days
    ten_days = add_achievement("Agate", "10 Days Digging", 'icons/Achievements/Agate.png', "You've been digging for ten days! That's a lot...I guess?")
    thirty_days = add_achievement("Jade", "30 Days Digging", 'icons/Achievements/Jade.png', "Woah, you like shinies!")
    fifty_days = add_achievement("Saphire", "50 Days Digging", 'icons/Achievements/Saphire.png', "Dude, it's becoming an addiction...")
    hundred_days = add_achievement("Ruby", "100 Days Digging", 'icons/Achievements/Ruby.png', "I think your family might be wondering were you are, shall I just tell them 'A Mine'? ")
    strong = add_achievement("Diamond", "500 Days Digging", 'icons/Achievements/Diamond.png', "I'm gonna go now...")

    #Mines
    mines1 = add_achievement("Bronze Medal - Mine Guide", "50 Mines", 'icons/Achievements/BronzeM.png', "You've been through 50 mines already!")
    mines2 = add_achievement("Silver Medal - Mole", "100 Mines", 'icons/Achievements/SilverM.png', "I know the mines better than the surface!")
    mines3 = add_achievement("Gold Medal - Into Deep", "300 Mines", 'icons/Achievements/GoldM.png', "Surface? What's 'Surface'?")

    for u in UserProfile.objects.all():
        print u


def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    return u


def add_user_profile(user, picture, location, equipment, vehicle, tool, all_time_max_gold, games_played, average, mines):
    up = UserProfile.objects.get_or_create(user=user, picture=picture, location=location,
                                           equipment=equipment, vehicle=vehicle, tool=tool,
                                           all_time_max_gold=all_time_max_gold, games_played=games_played,
                                           average=average, mines=mines)[0]
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