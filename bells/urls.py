from django.conf.urls import include
from django.contrib.sitemaps import views as sitemaps_views
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import home, about
from .sitemap import sitemaps


urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('methods/', include(('methods.urls', 'methods'), namespace='methods')),
    path('search/', include('haystack.urls')),
]

# sitemap bits - now cached as sitemap was HUGE and slow...
urlpatterns += [
    path(
        'sitemap.xml',
        cache_page(86400)(sitemaps_views.index),
        {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'},
        name='sitemap_url'
    ),
    path(
        'sitemap-<section>.xml',
        cache_page(86400)(sitemaps_views.sitemap),
        {'sitemaps': sitemaps},
        name='sitemaps'
    ),
]
