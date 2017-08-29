import logging
import random

from django.core.cache import cache
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Max, Min
from django.views.generic import DetailView, ListView

from .models import Method, MethodSet

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

        if 'count' in cache:
            count = cache.get('count')
        else:
            count = self.get_queryset().count()
            cache.set('count', count)

        if count:
            random_index = random.randint(0, count - 1)
            return Method.objects.get(pk=random_index)
        return None


class MethodListView(ListView):
    model = Method
    paginate_by = 100
    template_name = 'methods/method_list.html'

    def get_queryset(self):
        """
        Only get Methods for a given number of bells (order).
        """
        if 'order' in self.kwargs:
            return Method.objects.filter(method_set__p_stage=self.kwargs['order'])
        return Method.objects.all()


class MethodSetListView(ListView):
    model = MethodSet

    def readable_slug(self, slug):
        slug = slug.replace('-methods', ' ')
        slug = slug.replace('-', ' ')
        slug = ' '.join((s.capitalize() for s in slug.split(' ')))
        return slug

    def get_queryset(self):
        if 'slug' in self.kwargs:
            self.kwargs['order'] = self.readable_slug(self.kwargs['slug'])
            return Method.objects.filter(method_set__slug=self.kwargs['slug'])
        return MethodSet.objects.all()


def order_list_view(request, template='method/method_order_list.html'):
    logger.debug('order_list_view')

    max_nbells = max(MethodSet.objects.all().aggregate(Max('p_stage'))['p_stage__max'], 1)
    min_nbells = MethodSet.objects.all().aggregate(Min('p_stage'))['p_stage__min'] or 1

    orders = []
    for i in range(min_nbells, max_nbells + 1):
        count = Method.objects.filter(method_set__p_stage=i).count()
        orders.append([i, count])

    sum_count = sum([o[1] for o in orders])

    return render_to_response(template,
                              {'orders': orders, 'count': sum_count},
                              context_instance=RequestContext(request))
