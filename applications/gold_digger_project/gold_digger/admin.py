from django.contrib import admin
from gold_digger.models import UserProfile, ScanningEqipment
from django.contrib.auth.models import User

class UserAdmin2 (admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')

class GoldAdmin(admin.ModelAdmin):

    list_display = ('user', 'picture', 'location')
    readonly_fields = ('image_tag',)

class ScanAdmin (admin.ModelAdmin):
    list_display = ('name', 'modifier')
    readonly_fields = ('image_tag',)


admin.site.register(UserProfile, GoldAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin2)
admin.site.register(ScanningEqipment, ScanAdmin)

