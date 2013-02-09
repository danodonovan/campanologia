from django.conf.urls.defaults import patterns, url

from .views import MethodView, MethodInfoView, RandomMethodView, MethodListView, MethodSetListView

urlpatterns = patterns('methods.urls',
    # url(r'order/(?P<order>.*)/$', order_view, name='order'),
    # url(r'order/$', order_list_view, name='order_list'),
    # url(r'set/(?P<slug>.*)/$', method_set_view, name='method_set'),
    # url(r'sets/$', method_sets_view, name='method_sets'),
    # class based views
    url(
        regex=r'order/(?P<order>.*)$',
        view=MethodListView.as_view(),
        name='order'
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