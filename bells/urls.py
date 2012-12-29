from django.conf.urls import patterns, include, url
from django.contrib import admin

from bells.views import home

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    # Examples:
    url(r'^methods/', include('methods.urls', namespace='methods', app_name='methods')),
    # url(r'^methods/', include('methods.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
