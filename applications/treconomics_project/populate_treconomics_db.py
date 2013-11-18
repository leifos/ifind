__author__ = 'leif'
import os
import sys

def populate():

    print 'Adding Task Descriptions'
    add_task(topic_num='303',title='Hubble Telescope Achievements',description='<p>Identify positive accomplishments of the Hubble telescope since it was launched in 1991. </p><p>Documents are relevant that show the Hubble telescope has producednew data, better quality data than previously available, data that has increased human knowledge of the universe, or data that has led to disproving previously existing theories or hypotheses.</p><p>  Documents limited to the shortcomings of the telescope would be irrelevant.</p><p> Details of repairs or modifications to the telescope without reference to positive achievements would not be relevant.</p>')
    add_task(topic_num='307',title='New Hydroelectric Projects',description='<p>Identify hydroelectric projects proposed or under construction by country and location.</p><p>  Detailed description of nature, extent, purpose, problems, and consequences is desirable. Relevant documents would contain as a minimum a clear statement that a hydroelectric project is planned or construction is under way and the location of the project. </p><p> Renovation of existing facilities would be judged not relevant unless plans call for a significant increase in acre-feet or reservoir or a marked change in the environmental impact of the project.</p><p>  Arguments for and against proposed projects are relevant as long as they are supported by specifics, including as a minimum the name or location of the project.</p><p>  A statement that an individual or organization is for or against such projects in general would not be relevant.</p><p>  Proposals or projects underway to dismantle existing facilities or drain existing reservoirs are not relevant, nor are articles reporting a decision to drop a proposed plan.</p>')
    add_task(topic_num='310',title='Radio Waves and Brain Cancer',description='<p>Evidence that radio waves from radio towers or car phones affect brain cancer occurrence. </p><p> Persons living near radio towers and more recently persons using car phones have been diagnosed with brain cancer. </p><p> The argument rages regarding the direct association of one with the other. </p><p>The incidence of cancer among the groups cited is considered, by some, to be higher than that found in the normal population. </p><p> A relevant document includes any experiment with animals, statistical study, articles, news items which report on the incidence of brain cancer being higher/lower/same as those persons who live near a radio tower and those using car phones as compared to those in the general population.</p>')
    add_task(topic_num='314',title='Marine Vegetation',description='<p>Commercial harvesting of marine vegetation such as algae, seaweed and kelp for food and drug purposes. </p><p>Recent research has shown that marine vegetation is a valuable source of both food (human and animal) and a potentially useful drug. </p><p> This search will focus primarily on these two uses.</p><p>  Also to be considered relevant would be instances of other possible commercial uses such as fertilizer, etc.</p>')
    add_task(topic_num='322',title='International Art Crime',description='<p>Isolate instances of fraud or embezzlement in the international art trade. </p><p>A relevant document is any report that identifies an instance of fraud or embezzlement in the international buying or selling of art objects. </p><p> Objects include paintings, jewelry, sculptures and any other valuable works of art. </p><p> Specific instances must be identified for a document to be relevant; generalities are not relevant.</p>')
    add_task(topic_num='347',title='Wildlife Extinction',description='<p>The spotted owl episode in America highlighted U.S. efforts to prevent the extinction of wildlife species.</p><p>  What is not well known is the effort of other countries to prevent the demise of species native to their countries. </p><p> What other countries have begun efforts to prevent such declines?</p><p>A relevant item will specify the country, the involved species, and steps taken to save the species.</p>')
    add_task(topic_num='383',title='Mental Illness Drugs',description='<p>Identify drugs used in the treatment of mental illness. </p><p>A relevant document will include the name of a specific or generic type of drug.  Generalities are not relevant.</p>')
    add_task(topic_num='435',title='Curbing Population Growth',description='<p>What measures have been taken worldwide and what countries have been effective in curbing population growth? </p><p>A relevant document must describe an actual case in which population measures have been taken and their results are known  the reduction measures must have been actively pursued; that is, passive events such as disease or famine involuntarily reducing the population are not relevant.</p>')
    add_task(topic_num='344',title='Abuses of E-Mail',description='<p>The availability of E-mail to many people through their job or school affiliation has allowed for many efficiencies in communications but also has provided the opportunity for abuses.</p><p>  What steps have been taken world-wide by those bearing the cost of E-mail to prevent excesses?</p><p> To be relevant, a document will concern dissatisfaction by an entity paying for the cost of electronic mail.</p><p>  Particularly sought are items which relate to system users (such as employees) who abuse the system by engaging in communications of the type not related to the payer\'s desired use of the system.</p>')
    add_task(topic_num='999',title='Test Topic',description='<p>Test topic - find documents about tests.</p>')
    add_task(topic_num='367',title='Piracy',description='<p>What modern instances have there been of old fashioned piracy, the boarding or taking control of boats?</p><p>Documents discussing piracy on any body of water are relevant.</p><p> Documents discussing the legal taking of ships or their contents by a national authority are non-relevant.</p><p>  Clashes between fishing vessels overfishing are not relevant, unless one vessel is boarded.</p>')

    print 'Adding Test Users'
    add_user('t1','1',1,0,1,'')
    add_user('t2','2',2,0,1,'')
    add_user('t3','3',3,2,1,'')
    add_user('t4','4',4,2,1,'')
    add_user('a1','1',4,0,1,'')
    add_user('a2','2',4,0,0,'')
    add_user('a3','3',5,2,1,'')
    add_user('a4','4',5,2,0,'')
    add_user('d1','1',6,0,1,'')
    add_user('d2','2',6,0,0,'')
    add_user('d3','3',7,0,1,'')
    add_user('d4','4',7,0,0,'')
    add_user('d5','5',8,0,1,'')
    add_user('d6','6',8,0,0,'')
    add_user('d7','7',9,0,1,'')
    add_user('d8','8',9,0,0,'')


def add_user(username,password, condition, experiment, rotation, data=None):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    up = UserProfile.objects.get_or_create(user=u, condition=condition, experiment=experiment, rotation=rotation, data=data)[0]
    print "\t %s" % (u)

def add_task(topic_num, title, description):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num, title=title, description=description)[0]
    print "\t %s" % (t)
    return t


if __name__ == '__main__':
    print "Starting Treconomics population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')
    from treconomics.models import TaskDescription
    from treconomics.models import UserProfile
    from django.contrib.auth.models import User
    populate()