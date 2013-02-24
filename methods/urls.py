from django.conf.urls import patterns, url

from .views import MethodView, MethodInfoView, RandomMethodView, MethodListView, MethodSetListView


urlpatterns = patterns('methods.urls',
    # class based views
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
        regex=r'sets/',
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
)