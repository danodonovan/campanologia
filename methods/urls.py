from django.conf.urls.defaults import patterns, url

from methods.views import method_view, order_view

urlpatterns = patterns('methods.urls',
    url(r'order/(?P<order>.*)/$', order_view, name='order'),
    url(r'(?P<slug>.*)/$', method_view, name='single_method'),
)