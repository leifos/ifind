__author__ = 'jim'
from pagefetch.models import Status, Category, Reward, Schools, Deals
import datetime

# Player statuses
Status.objects.all().delete() #Clear old statuses
Status(status_string="Chasing Chihuahua", icon="", points_required=1000).save()
Status(status_string="Seeking Shitzu", icon="", points_required=2500).save()
Status(status_string="Pursuing Poodle", icon="", points_required=5000).save()
Status(status_string="Rummaging Rottweiler", icon="", points_required=7500).save()
Status(status_string="Tracking Terrier", icon="", points_required=10000).save()
Status(status_string="Dingo Detective", icon="", points_required=25000).save()
Status(status_string="Browsing Bulldog", icon="", points_required=50000).save()
Status(status_string="Searching Spaniel", icon="", points_required=75000).save()
Status(status_string="Discovering Dane", icon="", points_required=100000).save()
Status(status_string="Hunting Hound", icon="", points_required=1000000).save()
print "Populated statuses."

Category.objects.all().delete() #Clear old categories
Category(category="Sport", icon="", active=True).save()
Category(category="TV", icon="", active=True).save()
Category(category="Politics", icon="", active=True).save()
Category(category="Actors", icon="", active=True).save()
Category(category="Games", icon="", active=True).save()
Category(category="News", icon="", active=True).save()
Category(category="Movies", icon="", active=True).save()
Category(category="Shopping", icon="", active=True).save()
Category(category="Music", icon="", active=True).save()
print "Populated categories."

# Deals
Deals.objects.all().delete()
Deals(offer_text="Win an iPod", conditions_text="Must be 12 years or under.", active=True, icon="", expiry=datetime.datetime.now()).save()
Deals(offer_text="Win a speedboat", conditions_text="Must be over 18 years.", active=True, icon="", expiry=datetime.datetime.now()).save()

print "Populated deals."

# Rewards
Reward.objects.all().delete() #Clear old rewards
Reward(reward="None", icon="", points_required=0).save()
Reward(reward="Bronze", icon="", points_required=2500).save()
Reward(reward="Silver", icon="", points_required=5000).save()
Reward(reward="Gold", icon="", points_required=10000).save()
print "Populated rewards."

# Schools
Schools.objects.all().delete() #Clear old rewards
Schools(school_name = "Vale of Leven Academy", location="Alexandria, Scotland").save()
Schools(school_name = "Eastwood High School", location="Glasgow, Scotland").save()
Schools(school_name = "University of Glasgow", location="Glasgow, Scotland").save()
print "Populated schools."

