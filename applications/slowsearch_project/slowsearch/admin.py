__author__ = 'Craig'
from django.contrib import admin
from slowsearch.models import UKDemographicsSurvey, Experience


admin.site.register(UKDemographicsSurvey)
admin.site.register(Experience)