import logging

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template  import RequestContext
from django.template.loader import render_to_string
from django.views.generic import DetailView

from methods.models import Method, MethodOrderCount

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

def order_view(request, order):
    logger.debug('order_view <order> %s' % order)
    methods = get_list_or_404(Method, nbells=order)
    order = MethodOrderCount.objects.filter(order=order).latest()

    return render_to_response('method/method_list.html',
        {'order':order, 'methods':methods},
        context_instance=RequestContext(request))


class MethodView(DetailView):
    """ Generic detail view for a single member lab
    """

    context_object_name = 'method'
    template_name       = 'method/method.html'

    model = Method
    slug_field = 'slug'

    queryset = Method.objects.all()