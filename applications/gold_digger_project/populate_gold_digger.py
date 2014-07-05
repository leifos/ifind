import os


def populate():

    lamp = add_scanning_equipment('Oil lamp', 0.2, 'icons/Oil lamp.png', 10)
    add_scanning_equipment('Map', 0.3, 'icons/Map.png', 10)
    add_scanning_equipment('Sonar', 0.5, 'icons/Sonar.gif', 10)
    dwarf = add_scanning_equipment('Guide Dwarf', 0.6, 'icons/Guide Dwarf.png', 10)
    spell = add_scanning_equipment('Spell', 0.8, 'icons/Spell.png', 10)

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', spell)
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', lamp)
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', dwarf)




    for u in UserProfile.objects.all():
        print u


def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    return u


def add_user_profile(user, picture, location, equipment):
    up = UserProfile.objects.get_or_create(user=user, picture=picture, location=location, equipment=equipment)[0]
    return up


def add_scanning_equipment(name, modifier, image, price):
    eq = ScanningEqipment.objects.get_or_create(name=name, modifier=modifier, image=image, price=price)[0]
    return eq

if __name__ == '__main__':
    print "Starting Gold Digger population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_digger_project.settings')
    from gold_digger.models import UserProfile, ScanningEqipment
    from django.contrib.auth.models import User
    populate()