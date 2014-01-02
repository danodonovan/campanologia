import logging
import random

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Max, Min
from django.views.generic import DetailView, ListView

from .models import Method #, MethodSet

logger = logging.getLogger('django_debug')


class MethodView(DetailView):
    model = Method


class MethodInfoView(MethodView):
    """
    MethodInfoView - as MethodView but with different template
    """
    template_name = 'methods/method_info.html'


class RandomMethodView(MethodView):
    """
    RandomMethodView
        inherits from MethodView, but returns random Method from DB
        trying to efficiently choose Method using caching
    """
    def get_object(self, queryset=None):
        count = cache.get('count') or cache.set('count', self.get_queryset().count()) or cache.get('count')
        random_index = random.randint(0, count - 1)
        return Method.objects.get(pk=random_index)


class MethodListView(ListView):
    model = Method
    paginate_by = 100
    template_name = 'methods/method_list.html'

    def get_queryset(self):
        """
        Only get Methods for a given number of bells (order).
        """
        if 'order' in self.kwargs:
            return Method.objects.filter(ms_p_stage=self.kwargs['order'])
        return Method.objects.all()

# class MethodSetListView(ListView):
#     model = MethodSet
#
# class MethodOrderListView(ListView):
#     model = Method

def order_list_view(request, template='method/method_order_list.html'):
    logger.debug('order_list_view')

    max_nbells = Method.objects.all().aggregate(Max('ms_p_stage'))['ms_p_stage__max']
    min_nbells = Method.objects.all().aggregate(Min('ms_p_stage'))['ms_p_stage__min']
    # max_nbells = MethodSet.objects.all().aggregate(Max('p_stage'))['p_stage__max']
    # min_nbells = MethodSet.objects.all().aggregate(Min('p_stage'))['p_stage__min']

    orders = []
    for i in range(min_nbells, max_nbells+1):
        count = Method.objects.filter(ms_p_stage=i).count()
        orders.append([i, count])

    sum_count = sum([o[1] for o in orders])

    return render_to_response(template,
                              {'orders': orders, 'count': sum_count },
                              context_instance=RequestContext(request))