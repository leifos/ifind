from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    SPELL = 0.8
    GOBLIN = 0.6
    SONAR = 0.5
    MAP = 0.3
    OIL_LAMP = 0.2

    EQUIPMENT =(
        (SPELL, 'Spell'),
        (GOBLIN, 'Goblin'),
        (SONAR, 'Sonar'),
        (MAP, 'Map'),
        (OIL_LAMP, 'Oil lamp'),
    )

    WHEELBARREL = 'Wheelbarrel'
    MULE = 'Mule'
    CART = 'Cart'
    TRUCK = 'Truck'
    MECHA = 'Mecha'

    VEHICLE = (
        (WHEELBARREL, 'Wheelbarrel'),
        (MULE, 'Mule'),
        (CART, 'Cart'),
        (TRUCK, 'Truck'),
        (MECHA, 'Mecha'),
    )


    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_pictures', blank=True, default='profile_pictures/default_profile.jpg')
    location = models.CharField(max_length = 100)
    equipment = models.CharField(max_length=10, choices=EQUIPMENT, default=OIL_LAMP)
    vehicle = models.CharField(max_length=15, choices=VEHICLE, default=WHEELBARREL)
    gold = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.picture.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.user.username