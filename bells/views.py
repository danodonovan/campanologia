import logging

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template  import RequestContext

from methods.models import MethodOrderCount

logger = logging.getLogger('django_debug')

def home(request):
    logger.debug('home')

    orders =  MethodOrderCount.objects.order_by('order')

    return render_to_response('home.html',
        {'orders': orders},
        context_instance=RequestContext(request))

