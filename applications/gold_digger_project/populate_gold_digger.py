import os


def populate():

    lamp = add_scanning_equipment('Oil lamp', 0.2, 'icons/Scan/Oil lamp.png', 10)
    map = add_scanning_equipment('Map', 0.3, 'icons/Scan/Map.png', 10)
    sonar = add_scanning_equipment('Sonar', 0.5, 'icons/Scan/Sonar.gif', 10)
    dwarf = add_scanning_equipment('Guide Dwarf', 0.6, 'icons/Scan/Guide Dwarf.png', 10)
    spell = add_scanning_equipment('Spell', 0.8, 'icons/Scan/Spell.png', 10)

    shovel =add_digging_equipment('Shovel', 0.2, 'icons/Tools/Shovel_normal.png', 10)
    golden_shovel = add_digging_equipment('Golden Shovel', 0.4, 'icons/Tools/Shovel_golden.png', 10)
    dynamite = add_digging_equipment('Dynamite', 0.6, 'icons/Tools/Dynamite.png', 10)
    mecha = add_digging_equipment('Mecha', 0.8, 'icons/Tools/Mecha.png', 10)

    wheelbarrow = add_vehicle('Wheelbarrow', 0.2, 'icons/Vehicle/Wheelbarrow.png', 10)
    cart = add_vehicle('Cart', 0.4, 'icons/Vehicle/Cart.png', 10)
    donkey = add_vehicle('Donkey', 0.6, 'icons/Vehicle/Donkey.png', 10)
    truck = add_vehicle('Truck', 0.8, 'icons/Vehicle/Truck.png', 10)

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', spell, wheelbarrow, shovel, 1234, 4, 308.5)
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', lamp, cart, golden_shovel, 345, 10, 34.5)
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', dwarf, truck, mecha, 567, 7, 1000)




    for u in UserProfile.objects.all():
        print u


def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    return u


def add_user_profile(user, picture, location, equipment, vehicle, tool, all_time_max_gold, games_played, average):
    up = UserProfile.objects.get_or_create(user=user, picture=picture, location=location,
                                           equipment=equipment, vehicle=vehicle, tool=tool,
                                           all_time_max_gold=all_time_max_gold, games_played=games_played,
                                           average=average)[0]
    return up


def add_scanning_equipment(name, modifier, image, price):
    eq = ScanningEquipment.objects.get_or_create(name=name, modifier=modifier, image=image, price=price)[0]
    return eq

def add_digging_equipment(name, modifier, image, price):
    deq = DiggingEquipment.objects.get_or_create(name=name, modifier=modifier, image=image, price=price)[0]
    return deq

def add_vehicle(name, modifier, image, price):
    vehicle = Vehicle.objects.get_or_create(name=name, modifier=modifier, image=image, price=price)[0]
    return vehicle

if __name__ == '__main__':
    print "Starting Gold Digger population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_digger_project.settings')
    from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle
    from django.contrib.auth.models import User
    populate()