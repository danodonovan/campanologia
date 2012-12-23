from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import direct_to_template

from method.views import MethodView, method_view, order_view

urlpatterns = patterns('method.urls',
    url(r'order/(?P<order>.*)/$', order_view, name='order'),
    url(r'(?P<slug>.*)/$', method_view, name='method'),
)