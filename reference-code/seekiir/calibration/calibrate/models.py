from django.db import models

# Create your models here.
class TestCollection(models.Model):
    name = models.CharField(max_length=30)
    type = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name + ' ' + self.type

class Topic(models.Model):
    testcollection = models.ForeignKey(TestCollection)
    num = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    desc = models.TextField()
    summary = models.CharField(max_length=200)

    def __unicode__(self):
        return self.num + ' ' + self.title


class Document(models.Model):
    topic = models.ForeignKey(Topic)
    docid = models.CharField(max_length=40)
    title = models.CharField(max_length=150)
    text = models.TextField()
    snippet = models.CharField(max_length=200)
    relevant = models.IntegerField(default=0)

    def __unicode__(self):
        return self.docid + ' ' + self.title

