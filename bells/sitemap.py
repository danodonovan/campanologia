#! /usr/bin/env python
import os
from datetime import datetime

from django.conf import settings
from django.contrib.sitemaps import Sitemap

from methods.models import Method, MethodSet

class StaticSitemap(Sitemap):
    priority = 0.5

    # set lastmod to the mod time of the last file changed in the template dir
    lastmod = datetime.fromtimestamp(0)
    for template_dir in settings.TEMPLATE_DIRS:
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                filepath = os.path.join(root, file)
                newmod = datetime.fromtimestamp(os.stat(filepath).st_mtime)
                lastmod = newmod if newmod > lastmod else lastmod

    def items(self):
        return [
            "/",
            "/about",
        ]

    def location(self, obj):
        return obj[0] if isinstance(obj, tuple) else obj

    def changefreq(self, obj):
        return obj[1] if isinstance(obj, tuple) else "monthly"

class BaseSitemap(Sitemap):
    priority = 0.5
    changefreq = "monthly"

    def location(self, obj):
        return obj.get_absolute_url()

    def lastmod(self, obj):
        return MethodSet.objects.latest().updated

class MethodSitemap(BaseSitemap):
    changefreq = "monthly"

    def items(self):
        return Method.objects.all()

class MethodOrderCountSitemap(BaseSitemap):
    changefreq = "monthly"

    def items(self):
        return MethodSet.objects.all()


sitemaps = {
    'static': StaticSitemap,
    'methods': MethodSitemap,
    #'order': MethodOrderCount,
}
