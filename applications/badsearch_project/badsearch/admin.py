from django.contrib import admin
from badsearch.models import UserProfile, Demographics

admin.site.register(UserProfile),
admin.site.register(Demographics)