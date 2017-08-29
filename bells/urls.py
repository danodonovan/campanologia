#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from django.conf.urls import include, url
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page

from .views import home, about
from .sitemap import sitemaps

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^about/', about, name='about'),
    url(r'^methods/', include('methods.urls', namespace='methods', app_name='methods')),
    url(r'^search/', include('haystack.urls'), name='haystack_search'),
]

# sitemap bits - now cached as sitemap was HUGE and slow...
urlpatterns += [
    url(r'^sitemap\.xml$',
        cache_page(86400)(sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(86400)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps}, name='sitemaps'),
]
