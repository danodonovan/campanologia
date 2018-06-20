import logging

from django.conf import settings
from django.shortcuts import render

from methods.views import order_list_view

logger = logging.getLogger('django_debug')


def home(request):
    logger.debug('home')

    return order_list_view(request, template='home.html', dev=settings.DEBUG)


def about(request):
    logger.debug('about')

    return render(request, 'about.html')
