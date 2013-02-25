from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap as sitemap_view
from bells.views import home, about
from bells.sitemap import sitemaps

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^about/', about, name='about'),
    url(r'^methods/', include('methods.urls', namespace='methods', app_name='methods')),
    url(r'^search/', include('haystack.urls')),
    # sitemap for SEO
    url(r'^sitemap\.xml$', sitemap_view, {'sitemaps': sitemaps}, name='sitemap')
)
