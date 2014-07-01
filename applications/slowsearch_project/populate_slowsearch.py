__author__ = 'Craig'

import os
import datetime

now = datetime.datetime.today()


def populate():
    # add the users for testing
    dave = User.objects.create_user('dave', 'dave@dave.com', 'dave')
    dave_profile = add_profile(dave, now, 1)
    john = User.objects.create_user('john', 'john@john.com', 'john')
    john_profile = add_profile(john, now, 2)
    stan = User.objects.create_user('stan', 'stan@stan.com', 'stan')
    stan_profile = add_profile(stan, now, 3)

    dave_demog = add_demog(dave, 25, 'M', 'Yes', 'Biology', 'Completed')
    john_demog = add_demog(john, 30, 'M', 'No', '', '')
    stan_demog = add_demog(stan, 20, 'M', 'Yes', 'Maths', 'Third Year')

    dave_exp = add_experience(dave, 'A', 'U', 'D', 'A', 'D', 'D', 'U', 'A', 'Easy to use but slow at times')
    john_exp = add_experience(john, 'D', 'A', 'A', 'A', 'D', 'U', 'A', 'A', 'The interface frightened me')
    stan_exp = add_experience(stan, 'U', 'A', 'A', 'D', 'U', 'A', 'U', 'D', 'Google > Bing')


def add_demog(user, age, sex, ed_ug, ed_ug_maj, ed_ug_yr):
    d = UKDemographicsSurvey.objects.get_or_create(
        user=user, age=age, sex=sex, education_undergrad=ed_ug, education_undergrad_major=ed_ug_maj,
        education_undergrad_year=ed_ug_yr)
    return d


def add_experience(user, ease, boredom, rage, frustration, excitement, indifference, confusion, anxiety, comment):
    e = Experience.objects.get_or_create(user=user, ease=ease, boredom=boredom, rage=rage, frustration=frustration,
                                         excitement=excitement, indifference=indifference, confusion=confusion,
                                         anxiety=anxiety, comment=comment)
    return e


def add_profile(user, user_since, condition):
    p = UserProfile.objects.get_or_create(user=user, user_since=user_since, condition=condition)
    return p


if __name__ == '__main__':
    print "Starting slowsearch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slowsearch_project.settings')
    from slowsearch.models import User, UKDemographicsSurvey, Experience, UserProfile
    populate()


