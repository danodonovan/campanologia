import logging
import random

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template  import RequestContext
from django.template.loader import render_to_string
from django.views.generic import DetailView

from .models import Method, MethodSet, FirstTowerbellPeal, FirstHandbellPeal

logger = logging.getLogger('django_debug')

def method_view(request, slug):
    logger.debug('method_view <slug> %s' % slug)
    method = get_object_or_404(Method, slug__iexact=slug)

    javascript = render_to_string('js/blueline.js', {'method': method})

    return render_to_response('method/method.html',
        {'method': method, 'js_blueline':javascript},
        context_instance=RequestContext(request))

def match_view(request, match):
    logger.debug('match_view <match> %s' % match)
    methods = get_list_or_404(Method, name__icontains=match)

    return render_to_response('method/method_list.html',
        {'match':match, 'method':methods},
        context_instance=RequestContext(request))

def random_view(request, order=None):
    logger.debug('random_view <order> %s' % order)

    methods = Method.objects.all()
#    if not order:
#        methods = Method.objects.all()
#    else:
#        methods = Method.objects.filter(nbells=order)

    # sort_by('?') will kill the SQL performance
    count = methods.count()
    random_index = random.randint(0, count - 1)
    method = methods[random_index]

    javascript = render_to_string('js/blueline.js', {'method': method})

    return render_to_response('method/method.html',
        {'method': method, 'js_blueline':javascript},
        context_instance=RequestContext(request))

def order_view(request, order):
    logger.debug('order_view <order> %s' % order)
    # methods = get_list_or_404(MethodSet, p_stage=order)
    # order = MethodSet.objects.filter(p_stage=order)
    # Method.objects.filter(method_set__id=ms[0].id)
    methods = Method.objects.filter(method_set__p_stage=order)

    return render_to_response('method/method_list.html',
        {'order':order, 'methods':methods},
        context_instance=RequestContext(request))


#class MethodView(DetailView):
#    """ Generic detail view for a single member lab
#    """
#
#    context_object_name = 'method'
#    template_name       = 'method/method.html'
#
#    model = Method
#    slug_field = 'slug'
#
#    queryset = Method.objects.all()