from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    user = models.OneToOneField(User)

    picture = models.ImageField(upload_to='profile_pictures', blank=True)
    location = models.CharField(max_length = 100)

    def image_tag(self):
        return u'<img src="%s" height = 100 />' % (self.picture.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __unicode__(self):
        return self.user.username