import os


def populate():

    ### SCANNING ###

    lamp = add_scanning_equipment('Oil lamp', 0.2, 'icons/Scan/Oil lamp.png', 1, "It won't allow you to see much but it's better than going in blind!", 20)
    map = add_scanning_equipment('Map', 0.3, 'icons/Scan/Map.png', 100, "It probably helps knowing you're not digging in the wrong place", 30)
    sonar = add_scanning_equipment('Sonar', 0.5, 'icons/Scan/Sonar.gif', 500, "Now we're cooking with gas!", 50)
    dwarf = add_scanning_equipment('Guide Dwarf', 0.6, 'icons/Scan/Guide Dwarf.png', 800, "If you're not sure, just ask the locals!", 60)
    spell = add_scanning_equipment('Spell', 0.8, 'icons/Scan/Spell.png', 1000, "Magic beats science EVERY TIME", 80)

    ### DIGGING ###

    spoon  = add_digging_equipment('Spoon', 0.3, 8, 'icons/Tools/Spoon.png', 1, "What am I supposed to do with this?", 30)
    shovel = add_digging_equipment('Shovel', 0.4, 7, 'icons/Tools/Shovel_normal.png', 200, "It's a shovel", 40)
    golden_shovel = add_digging_equipment('Golden Shovel', 0.5, 6, 'icons/Tools/Shovel_golden.png', 300, "It might seem like a bad idea, but it's not REAL gold", 50)
    dynamite = add_digging_equipment('Dynamite', 0.6, 5, 'icons/Tools/Dynamite.png', 500, "KABLAMO!", 60)
    mecha = add_digging_equipment('Mecha', 0.8, 3, 'icons/Tools/Mecha.png', 1000, "Dig ALL the gold!", 80)

    ### MOVING ###

    boots = add_vehicle('Boots', 20, 'icons/Vehicle/Boots.png', 1, "Two boots is better than no boots!")
    wheelbarrow = add_vehicle('Wheelbarrow', 18, 'icons/Vehicle/Wheelbarrow.png', 300, "Well, if you start selling mussels too, you're set!")
    cart = add_vehicle('Cart', 15, 'icons/Vehicle/Cart.png', 500, "Maybe don't ride it, it doesn't have breaks")
    donkey = add_vehicle('Donkey', 10, 'icons/Vehicle/Donkey.png', 800, "Nothing like good'ol animal power to carry your gold!")
    truck = add_vehicle('Truck', 5, 'icons/Vehicle/Truck.png', 1000, "They see me rollin'!")

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', spell, wheelbarrow, shovel, 1234, 0, 308.5, 0)
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', lamp, cart, golden_shovel, 345, 0, 34.5, 0)
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', dwarf, truck, mecha, 567, 0, 1000, 0)




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

if __name__ == '__main__':
    print "Starting Gold Digger population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_digger_project.settings')
    from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle
    from django.contrib.auth.models import User
    populate()