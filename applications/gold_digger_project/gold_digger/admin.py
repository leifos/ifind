from django.contrib import admin
from gold_digger.models import UserProfile, ScanningEquipment, DiggingEquipment, Vehicle, Achievements, UserAchievements
from django.contrib.auth.models import User

class UserAdmin2 (admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')

class GoldAdmin(admin.ModelAdmin):

    list_display = ('user', 'picture', 'location', 'mines')
    readonly_fields = ('image_tag',)

class ScanAdmin(admin.ModelAdmin):
    list_display = ('name', 'modifier', 'price')
    readonly_fields = ('image_tag',)

class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'modifier', 'price')
    readonly_fields = ('image_tag',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'modifier', 'price')
    readonly_fields = ('image_tag',)

class AchievementsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ('image_tag',)

class UserAchievementsAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement')


admin.site.register(UserProfile, GoldAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin2)
admin.site.register(ScanningEquipment, ScanAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(DiggingEquipment, ToolAdmin)
admin.site.register(Achievements, AchievementsAdmin)
admin.site.register(UserAchievements, UserAchievementsAdmin)



