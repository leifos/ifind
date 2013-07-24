from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls import patterns
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='index.html'))

)



    # Examples:
    # url(r'^$', 'searchlab_project.views.home', name='home'),
    # url(r'^searchlab_project/', include('searchlab_project.foo.urls')),
