from django.db import models
from django.contrib.auth.models import User


class ScanningEquipment(models.Model):
    name = models.CharField(max_length=100)
    modifier = models.FloatField(default=0.2)
    image = models.ImageField(upload_to='icons/Scan')
    price = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class DiggingEquipment(models.Model):

    name = models.CharField(max_length=100)
    modifier = models.FloatField(default=0.2)
    image = models.ImageField(upload_to='icons/Tools')
    price = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    modifier = models.FloatField(default=0.2)
    image = models.ImageField(upload_to='icons/Vehicle')
    price = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name



class UserProfile(models.Model):
    SPELL = 'Spell'
    GOBLIN = 'Goblin'
    SONAR = 'Sonar'
    MAP = 'Map'
    OIL_LAMP = 'Oil lamp'

    EQUIPMENT = (
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
    equipment = models.ForeignKey(ScanningEquipment)
    vehicle = models.ForeignKey(Vehicle)
    tool = models.ForeignKey(DiggingEquipment)
    gold = models.IntegerField(default=0)
    all_time_max_gold = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.picture.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.user.username


