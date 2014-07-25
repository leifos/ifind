import os
import datetime

now = datetime.datetime.today()

def populate():
    janedoe = User.objects.create_user('janedoe', 'janedoe@test.com', '1234')
    janedoe_profile = add_profile(janedoe, now, 1)
    johndoe = User.objects.create_user('johndoe', 'johndoe@test.com', '1234')
    johndoe_profile = add_profile(johndoe, now, 2)

    janedoe_demog = add_demog(janedoe, 29, 'F', 'Yes', 'Maths', 'Completed')
    johndoe_demog = add_demog(johndoe, 19, 'M', 'Yes', 'French', 'Fourth Year')


def add_demog(user, age, sex, ed_ug, ed_ug_maj, ed_ug_yr):
    d = Demographics.objects.get_or_create(
        user=user, age=age, sex=sex, education_undergrad=ed_ug, education_undergrad_major=ed_ug_maj,
        education_undergrad_year=ed_ug_yr)
    return d

def add_profile(user, user_since, condition):
    p = UserProfile.objects.get_or_create(user=user, user_since=user_since, condition=condition)
    return p

if __name__ == '__main__':
    print "Starting badsearch population script..."
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'badsearch_project.settings')
    from badsearch.models import User, Demographics, UserProfile
    populate()
