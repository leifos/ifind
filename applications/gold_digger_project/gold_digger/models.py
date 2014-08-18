from django.db import models
from django.contrib.auth.models import User


class ScanningEquipment(models.Model):
    name = models.CharField(max_length=100)
    modifier = models.FloatField(default=0.2)
    image = models.ImageField(upload_to='icons/Scan')
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    store_val = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class DiggingEquipment(models.Model):

    name = models.CharField(max_length=100)
    modifier = models.FloatField(default=0.2)
    time_modifier = models.IntegerField(default=8)
    image = models.ImageField(upload_to='icons/Tools')
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)
    store_val = models.IntegerField(default=0)


    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    modifier = models.IntegerField(default=10)
    image = models.ImageField(upload_to='icons/Vehicle')
    price = models.IntegerField(default=0)
    description = models.CharField(max_length=1000)



    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class UserProfile(models.Model):

    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_pictures', blank=True, default='profile_pictures/default_profile.jpg')
    location = models.CharField(max_length=100)
    equipment = models.ForeignKey(ScanningEquipment)
    vehicle = models.ForeignKey(Vehicle)
    tool = models.ForeignKey(DiggingEquipment)
    gold = models.IntegerField(default=100)
    all_time_max_gold = models.IntegerField(default=0)
    all_time_gold = models.IntegerField(default=0)
    games_played = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    mines = models.IntegerField(default=0)
    game_overs = models.IntegerField(default=0)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.picture.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.user.username


class Achievements(models.Model):
    name = models.CharField(max_length=100)
    condition = models.CharField(max_length=100)
    image = models.ImageField(upload_to='icons/Achievements')
    description = models.CharField(max_length=1000)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.name


class UserAchievements(models.Model):
    user = models.ForeignKey(UserProfile)
    achievement = models.ForeignKey(Achievements)

    def __unicode__(self):
        return self.achievement.name