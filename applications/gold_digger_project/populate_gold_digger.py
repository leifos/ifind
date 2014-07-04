import os


def populate():

    jill = add_user('Jill', 'jill@gmail.com', 'jill')
    john = add_user('John', 'john@gmail.com', 'john')
    jess = add_user('Jess', 'jess@gmail.com', 'jess')

    add_user_profile(jill, 'profile_pictures/FOW.jpg', 'Jesrsey', 'Spell')
    add_user_profile(john, 'profile_pictures/duck.jpg', 'NYC', 'Oil lamp')
    add_user_profile(jess, 'profile_pictures/penguinwhale.jpg', 'Detroit', 'Goblin')

    add_scanning_equipment('Oil lamp', 0.2, 'icons/Oil lamp.png')
    add_scanning_equipment('Map', 0.3, 'icons/Map.png')
    add_scanning_equipment('Sonar', 0.5, 'icons/Sonar.gif')
    add_scanning_equipment('Goblin', 0.6, 'icons/Goblin.png')
    add_scanning_equipment('Spell', 0.8, 'icons/Spell.png')


    for u in UserProfile.objects.all():
        print u


def add_user(username, email, password):
    u = User.objects.create_user(username=username, email=email, password=password)
    return u


def add_user_profile(user, picture, location, equipment):
    up = UserProfile.objects.get_or_create(user=user, picture=picture, location=location, equipment=equipment)[0]
    return up

def add_scanning_equipment(name, modifier, image):
    eq = ScanningEqipment.objects.get_or_create(name=name, modifier=modifier, image=image)
    return eq

if __name__ == '__main__':
    print "Starting Gold Digger population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gold_digger_project.settings')
    from gold_digger.models import UserProfile, ScanningEqipment
    from django.contrib.auth.models import User
    populate()