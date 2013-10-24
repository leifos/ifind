from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import models_experiments
# Create your models here.

class DocumentsExamined(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    docid = models.CharField(max_length=30)
    doc_num = models.CharField(max_length=30)
    judgement = models.IntegerField()
    url = models.CharField(max_length=200)
    judgement_date = models.DateTimeField('Date Examined')
    task = models.IntegerField(default=0)
    topic_num = models.IntegerField(default=0)
    def __unicode__(self):
        return self.docid

class TaskDescription(models.Model):
    topic_num = models.IntegerField(default=0)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1500)
    def __unicode__(self):
        return '%s' % (self.title)

class TopicQuerySuggestion(models.Model):
    topic_num = models.IntegerField(default=0)
    title = models.CharField(max_length=40)
    link = models.CharField(max_length=150)

    def __unicode__(self):
        return self.title


class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    # Other fields here
    data = models.CharField(max_length=200, null=True, blank=True)
    experiment = models.IntegerField(default=0)
    condition = models.IntegerField(default=0)
    rotation = models.IntegerField(default=0)
    tasks_completed = models.IntegerField(default=0)
    steps_completed = models.IntegerField(default=0)

    def __unicode__(self):
        return self.user.username

#def create_user_profile(sender, instance, created, **kwargs):
#    if created:
#        UserProfile.objects.create(user=instance)

#post_save.connect(create_user_profile, sender=User)