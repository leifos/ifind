from django.contrib import admin
from models import UserProfile, Demographics, Experience

admin.site.register(UserProfile),
admin.site.register(Demographics)
admin.site.register(Experience)