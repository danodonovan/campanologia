import logging
import random

from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.db.models import Max, Min

from .models import Method, MethodSet, FirstTowerbellPeal, FirstHandbellPeal

logger = logging.getLogger('django_debug')

def method_view(request, slug):
    logger.debug('method_view <slug> %s' % slug)
    method = get_object_or_404(Method, slug__iexact=slug)

    nbells = method.method_set.p_stage
    nchanges = (method.method_set.p_stage - method.method_set.p_numberOfHunts) * method.method_set.p_lengthOfLead
    notation = '%sLH%s' % (method.notation, method.leadHead)

    javascript = render_to_string('js/blueline.js',
                                  {'method': method, 'nbells': nbells, 'nchanges': nchanges, 'notation': notation})

    return render_to_response('method/method.html',
        {'method': method, 'js_blueline':javascript},
        context_instance=RequestContext(request))

def details_view(request, slug):
    logger.debug('method_view <slug> %s' % slug)
    method = get_object_or_404(Method, slug__iexact=slug)

    return render_to_response('method/method_detail.html', {'method': method},
                              context_instance=RequestContext(request))

def match_view(request, match):
    logger.debug('match_view <match> %s' % match)
    methods = get_list_or_404(Method, name__icontains=match)

    return render_to_response('method/method_list.html',
        {'match':match, 'method':methods},
        context_instance=RequestContext(request))

def order_list_view(request, template='method/method_order_list.html'):
    logger.debug('order_list_view')

    max_nbells = MethodSet.objects.all().aggregate(Max('p_stage'))['p_stage__max']
    min_nbells = MethodSet.objects.all().aggregate(Min('p_stage'))['p_stage__min']

    orders = []
    for i in range(min_nbells, max_nbells+1):
        count = Method.objects.filter(method_set__p_stage=i).count()
        orders.append([i, count])

    return render_to_response(template,
                              {'orders': orders, },
                              context_instance=RequestContext(request))

def random_view(request, order=None):
    logger.debug('random_view <order> %s' % order)

    methods = Method.objects.all()

    # sort_by('?') will kill the SQL performance
    count = methods.count()
    random_index = random.randint(0, count - 1)
    method = methods[random_index]
    nbells = method.method_set.p_stage
    nchanges = (method.method_set.p_stage - method.method_set.p_numberOfHunts) * method.method_set.p_lengthOfLead

    javascript = render_to_string('js/blueline.js',
          {'method': method, 'nbells': nbells, 'nchanges': nchanges})

    return render_to_response('method/method.html',
        {'method': method, 'js_blueline':javascript},
        context_instance=RequestContext(request))

def order_view(request, order):
    logger.debug('order_view <order> %s' % order)

    methods = Method.objects.filter(method_set__p_stage=order)

    return render_to_response('method/method_list.html',
        {'order': order, 'methods': methods},
        context_instance=RequestContext(request))

def method_set_view(request, slug):
    logger.debug('method_set_view <method_set> %slug' % slug)

    method_set = MethodSet.objects.get(slug=slug)
    methods = Method.objects.filter(method_set__slug=slug)

    return render_to_response('method/method_set_list.html',
                              {'method_set': method_set, 'methods': methods},
                              context_instance=RequestContext(request))

def method_sets_view(request):
    logger.debug('method_sets_view')

    method_sets = MethodSet.objects.all()

    return render_to_response('method/method_sets_list.html',
                              {'method_sets': method_sets,},
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