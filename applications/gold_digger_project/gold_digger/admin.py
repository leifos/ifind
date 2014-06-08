from django.contrib import admin
from gold_digger.models import UserProfile
from django.contrib.auth.models import User

class UserAdmin2 (admin.ModelAdmin):
    list_display = ('email', 'first_name')

class GoldAdmin(admin.ModelAdmin):

    list_display = ('user', 'picture', 'location')
    readonly_fields = ('image_tag',)



admin.site.register(UserProfile, GoldAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin2)
