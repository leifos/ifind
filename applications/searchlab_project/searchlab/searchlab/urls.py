from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'', include('search.urls')),
    url(r'^admin/', include(admin.site.urls)),

)



    # Examples:
    # url(r'^$', 'searchlab_project.views.home', name='home'),
    # url(r'^searchlab_project/', include('searchlab_project.foo.urls')),
