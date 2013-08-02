from django.conf.urls import url
from django.conf.urls import patterns
from django.views.generic import TemplateView

from .views import search, session

urlpatterns = patterns('search.views',

     url(regex=r'^$',
         view=TemplateView.as_view(template_name='index.html')
     ),

     url(regex=r'^search/$',
         view=search,
         name='search',
     ),

     url(regex=r'^session/$',
         view=session,
         name='session'
     )
)