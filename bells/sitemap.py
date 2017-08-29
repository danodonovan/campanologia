from django.contrib.sitemaps import GenericSitemap
from methods.models import Method, MethodSet

method_dict = {
    'queryset': Method.objects.all(),
}

method_set_dict = {
    'queryset': MethodSet.objects.all(),
}

sitemaps = {
    'methods': GenericSitemap(method_dict, priority=0.6, changefreq='never'),
    'method_sets': GenericSitemap(method_set_dict, priority=0.6, changefreq='never'),
}
