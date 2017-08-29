#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from django.conf.urls import url
from django.views.generic.base import RedirectView

from .views import MethodView, MethodInfoView, RandomMethodView, MethodListView, MethodSetListView


urlpatterns = [
    url(
       regex=r'order/(?P<order>(\d+))$',
       view=MethodListView.as_view(),
       name='order'
    ),
    url(
       regex='^order/(?P<order>(\d+))/(?P<page>(\d+))/$',
       view=MethodListView.as_view(),
       name='order_paginated'
    ),
    url(
       regex=r'sets/(?P<slug>.*)/$',
       view=MethodSetListView.as_view(),
       name='list_method_set',
    ),
    url(
       regex=r'random/',
       view=RandomMethodView.as_view(),
       name='random'
    ),
    url(
       regex=r'(?P<slug>.*)/$',
       view=MethodView.as_view(),
       name='single_method'
    ),
    url(
       regex=r'(?P<slug>.*)/details',
       view=MethodInfoView.as_view(),
       name='detail_method'
    ),
    url(
        regex=r'',
        view=RedirectView.as_view(pattern_name='haystack_search', permanent=False),
        name='search_redirect'
    )
]
