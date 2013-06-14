from django.db import models

# to avoid name collisions, I use QueryFilterM instead of QueryFilter
class QueryFilterM(models.Model):
    queryFilter = models.CharField(max_length=30)

    def __unicode__(self):
        return self.queryFilter

class ResultFilterM(models.Model):
    resultFilter = models.CharField(max_length=30)

    def __unicode__(self):
        return self.resultFilter

class SearchEngineM(models.Model):
    searchEngine = models.CharField(max_length=30)

    def __unicode__(self):
        return self.searchEngine

class Language(models.Model):
    LANGUAGE_CHOICES = (
        ('EN', 'English'),
        ('NL', 'Duch'),
    )
    language = models.CharField(max_length=2,choices = LANGUAGE_CHOICES)

    def __unicode__(self):
        return self.language

class QueryFilterOrder(models.Model):
    numOrder = models.IntegerField()
    queryFilter = models.ForeignKey(QueryFilterM)

    def __unicode__(self):
        return "Query filter: "+str(self.queryFilter)+" ("+str(self.numOrder)+")"
    

class ResultFilterOrder(models.Model):
    numOrder = models.IntegerField()
    resultFilter = models.ForeignKey(ResultFilterM)

    def __unicode__(self):
        return "Result filter: "+str(self.resultFilter)+" ("+str(self.numOrder)+")"

class SearchEngineUsed(models.Model):
    searchEngine = models.ForeignKey(SearchEngineM)

    def __unicode__(self):
        return "Search engine "+" "+str(self.searchEngine)

class ParameterQ(models.Model):
    queryFilterOrder = models.ForeignKey(QueryFilterOrder)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return " Parameter: "+self.key+" Value: "+self.value
                    
    
class ParameterR(models.Model):
    resultFilterOrder = models.ForeignKey(ResultFilterOrder)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return " Parameter: "+self.key+" Value: "+self.value                                     

class ParameterS(models.Model):
    searchEngineUsed = models.ForeignKey(SearchEngineUsed)
    key = models.CharField(max_length=20)
    value = models.CharField(max_length=100)

    def __unicode__(self):
        return " Parameter: "+self.key+" Value: "+self.value    
