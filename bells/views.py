import logging

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template  import RequestContext

from methods.models import Method, MethodSet

logger = logging.getLogger('django_debug')

def home(request):
    logger.debug('home')

    orders =  MethodSet.objects.order_by('p_stage')
    count = Method.objects.count()
    return render_to_response('home.html',
        {'orders': orders, 'count': count},
        context_instance=RequestContext(request))

def about(request):
    logger.debug('about')

    return render_to_response('about.html',
      context_instance=RequestContext(request))
