from django.views.generic.base import RedirectView
from django.urls import path

from .views import MethodView, MethodInfoView, RandomMethodView, MethodListView, MethodSetListView


urlpatterns = [
    path(
        route='order/<int:order>',
        view=MethodListView.as_view(),
        name='order'
    ),
    path(
        route='order/<int:order>/<int:page>',
        view=MethodListView.as_view(),
        name='order_paginated'
    ),
    path(
        route='sets/<slug>',
        view=MethodSetListView.as_view(),
        name='list_method_set',
    ),
    path(
        route='random',
        view=RandomMethodView.as_view(),
        name='random'
    ),
    path(
        route='<slug:slug>',
        view=MethodView.as_view(),
        name='single_method'
    ),
    path(
        route='<slug:slug>/details',
        view=MethodInfoView.as_view(),
        name='detail_method'
    ),
    path(
        route='',
        view=RedirectView.as_view(pattern_name='haystack_search', permanent=False),
        name='search_redirect'
    )
]
