__author__ = 'leif'

from django.contrib import admin
from ifind.models.game_models import Achievement, Category, CurrentGame, Page, UserProfile, Score, PlayerAchievement, Level

admin.site.register(Achievement)
admin.site.register(Category)
admin.site.register(CurrentGame)
admin.site.register(Page)
admin.site.register(UserProfile)
admin.site.register(Score)
admin.site.register(PlayerAchievement)
admin.site.register(Level)