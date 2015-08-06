__author__ = 'leif'
import os


def populate():
    print 'Adding Task Descriptions'
    add_task(topic_num='341',
             title='Airport Security',
             description='<p>In this practice task, '
                         'your job is to find articles '
                         'that discuss procedures airports '
                         'worldwide have taken to better '
                         'scrutinize passengers and their carry-on and checked luggage.</p>')
    add_task(topic_num='347',
             title='Wildlife Extinction',
             description='<p>For this task, your job is '
                         'to find articles that discuss efforts '
                         'made by countries other than the United States '
                         'to prevent the extinction of wildlife species '
                         'native to their countries.  </p>')
    add_task(topic_num='354',
             title='Journalist Risks',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances where journalists '
                         'have been put at risk '
                         '(e.g., killed, arrested or taken hostage) '
                         'in the performance of their work.</p>')
    add_task(topic_num='435',
             title='Curbing Population Growth',
             description='<p>For this task, your job '
                         'is to find articles that discuss countries '
                         'that have been successful in curbing population '
                         'growth and the measures they have taken to do so.</p>')
    add_task(topic_num='367',
             title='Piracy',
             description='<p>For this task, your job is to find '
                         'articles that discuss instances of piracy, '
                         'or the illegal boarding or taking control of a boat.</p>')

    # username, pw, condition, experiment, rotation, data
    print 'Adding Test Users'

    for i in range(0, 24):
        ut1 = 'test' + str(i)
        add_user(ut1, str(i), 0, 0, i, '')


def add_user(username, password, condition, experiment, rotation, data=None):
    u = User.objects.get_or_create(username=username)[0]
    u.set_password(password)
    u.save()
    up = \
        UserProfile.objects.get_or_create(user=u,
                                          condition=condition,
                                          experiment=experiment,
                                          rotation=rotation,
                                          data=data)[0]
    print '%s, %s, %d, %d  ' % (username, password, condition, rotation)


def add_task(topic_num, title, description):
    t = TaskDescription.objects.get_or_create(topic_num=topic_num,
                                              title=title,
                                              description=description)[0]
    print "\t %s" % t
    return t


if __name__ == '__main__':
    import django

    print "Starting Mickey's Treconomics population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'treconomics_project.settings')

    django.setup()
    from treconomics.models import TaskDescription
    from treconomics.models import UserProfile
    from django.contrib.auth.models import User


    populate()