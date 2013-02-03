from django.conf.urls.defaults import patterns, url

from methods.views import method_view, method_set_view, method_sets_view, order_view, order_list_view, random_view, details_view

urlpatterns = patterns('methods.urls',
    url(r'random/$', random_view, name='random'),
    url(r'random/(?P<order>.*)/$', random_view, name='random_with_order'),
    url(r'order/(?P<order>.*)/$', order_view, name='order'),
    url(r'order/$', order_list_view, name='order_list'),
    url(r'set/(?P<slug>.*)/$', method_set_view, name='method_set'),
    url(r'sets/$', method_sets_view, name='method_sets'),
    url(r'(?P<slug>.*)/details$', details_view, name='detail_method'),
    url(r'(?P<slug>.*)/$', method_view, name='single_method'),
)