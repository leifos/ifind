__author__ = 'leif'
from calibration import settings
from django.core.management import setup_environ
setup_environ(settings)
from calibrate.models import TestCollection, Topic, Document


TestCollection.objects.all().delete()
Topic.objects.all().delete()
Document.objects.all().delete()

tca = TestCollection(name='Aquaint', type='News')
tca.save()
tcb = TestCollection(name='TREC678', type='News')
tcb.save()
tcc = TestCollection(name='WT10G', type='Web')
tcc.save()
tcd = TestCollection(name='DotGov', type='Web')
tcd.save()

print tca

tc = TestCollection.objects.all()
for i in tc:
    print i


t1 = Topic(testcollection=tca, num='303', title='Hubble Telescope Achievements', summary='Identify positive accomplishments of the Hubble telescope since it was launched in 1991.', desc='Identify positive accomplishments of the Hubble telescope since it was launched in 1991. \n Documents are relevant that show the Hubble telescope has produced new data, better quality data than previously available, data that has increased human knowledge of the universe, or data that has led to disproving previously existing theories or hypotheses.\n\nDocuments limited to the shortcomings of the telescope would be irrelevant. \n\nDetails of repairs or modifications to the telescope without reference to positive achievements would not be relevant.\n' )
t1.save()
t2 = Topic(testcollection=tca, num='307', title='New Hydroelectric Projects',  summary='Identify hydroelectric projects proposed or under construction by country and location.', desc='Identify hydroelectric projects proposed or under construction by country and location.\n  Detailed description of nature, extent, purpose, problems, and consequences is desirable. Relevant documents would contain as a minimum a clear statement that a hydroelectric project is planned or construction is under way and the location of the project. \n Renovation of existing facilities would be judged not relevant unless plans call for a significant increase in acre-feet or reservoir or a marked change in the environmental impact of the project.\n  Arguments for and against proposed projects are relevant as long as they are supported by specifics, including as a minimum the name or location of the project.\n  A statement that an individual or organization is for or against such projects in general would not be relevant.\n  Proposals or projects underway to dismantle existing facilities or drain existing reservoirs are not relevant, nor are articles reporting a decision to drop a proposed plan.\n')
t2.save()
Topic(testcollection=tca, num='314', title='Marine Vegetation',summary='Commercial harvesting of marine vegetation such as algae, seaweed and kelp for food and drug purposes.',desc='Commercial harvesting of marine vegetation such as algae, seaweed and kelp for food and drug purposes. \nRecent research has shown that marine vegetation is a valuable source of both food (human and animal) and a potentially useful drug. \n This search will focus primarily on these two uses.\n  Also to be considered relevant would be instances of other possible commercial uses such as fertilizer, etc.\n').save()


t = Topic.objects.all()
for i in t:
    print i

Document(topic=t1, docid='AP123',title='Star Wars',text='Star wars initiative Star wars initiative Star wars initiative Star wars initiative Star wars initiative Star wars initiative',snippet='Star wars initiative',relevant=0).save()
Document(topic=t1, docid='AP144',title='Defense SDI',text='Star wars strategic defense intiaitive Star wars strategic defense intiaitive Star wars strategic defense intiaitive',snippet='Star wars strategic defense intiaitive',relevant=1).save()
Document(topic=t1, docid='AP154',title='Defense SDI',snippet='Star wars strategic defense intiaitive',relevant=1, text='Star wars strategic defense intiaitive Star wars strategic defense intiaitive Star wars strategic defense intiaitive').save()
Document(topic=t2, docid='AP523',title='Dams',text='Star wars initiative Star wars initiative Star wars initiative Star wars initiative Star wars initiative Star wars initiative',snippet='Star wars initiative',relevant=1).save()
Document(topic=t2, docid='AP644',title='Hydroelectic Project',text='Star wars strategic defense intiaitive Star wars strategic defense intiaitive Star wars strategic defense intiaitive',snippet='Star wars strategic defense intiaitive',relevant=1).save()
Document(topic=t2, docid='AP754',title='New Projects',snippet='Star wars strategic defense intiaitive',relevant=0, text='Star wars strategic defense intiaitive Star wars strategic defense intiaitive Star wars strategic defense intiaitive').save()


d = Document.objects.all()
for i in d:
    print i


