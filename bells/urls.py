from django.conf.urls import patterns, include, url

from bells.views import home, about

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^about/', about, name='about'),
    # Examples:
    url(r'^methods/', include('methods.urls', namespace='methods', app_name='methods')),
)
