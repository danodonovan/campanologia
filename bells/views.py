import logging

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template  import RequestContext

from methods.views import order_list_view

logger = logging.getLogger('django_debug')

def home(request):
    logger.debug('home')

    return order_list_view(request, template='home.html')

def about(request):
    logger.debug('about')

    return render_to_response('about.html',
      context_instance=RequestContext(request))
