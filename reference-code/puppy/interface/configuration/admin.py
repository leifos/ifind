from interface.configuration.models import QueryFilterM, ResultFilterM, SearchEngineM, Language,QueryFilterOrder, ResultFilterOrder, SearchEngineUsed, ParameterQ, ParameterR, ParameterS
from django.contrib import admin

#admin.site.register(QueryFilterM)
#admin.site.register(ResultFilterM)
#admin.site.register(SearchEngineM)
admin.site.register(Language)
#admin.site.register(QueryFilterOrder)
#admin.site.register(ResultFilterOrder)
#admin.site.register(SearchEngineUsed)
#admin.site.register(ParameterQ)
#admin.site.register(ParameterR)
#admin.site.register(ParameterS)

class ParameterQInline(admin.StackedInline):
  model = ParameterQ
  extra = 1

class QueryFilterOrderAdmin(admin.ModelAdmin):
  field = ['queryFilter', 'numOrder']
  inlines = [ParameterQInline]
  
admin.site.register(QueryFilterOrder,QueryFilterOrderAdmin)


class ParameterRInline(admin.StackedInline):
  model = ParameterR
  extra = 1

class ResultFilterOrderAdmin(admin.ModelAdmin):
  field = ['resultFilter', 'numOrder']
  inlines = [ParameterRInline]
  
admin.site.register(ResultFilterOrder,ResultFilterOrderAdmin)


class ParameterSInline(admin.StackedInline):
  model = ParameterS
  extra = 1

class SearchEngineUsedAdmin(admin.ModelAdmin):
  inlines = [ParameterSInline]
  
admin.site.register(SearchEngineUsed,SearchEngineUsedAdmin)
