from django.test import TestCase

from methods.models import Method, MethodSet

from .test_methodset import methodset_example


class MethodTestCase(TestCase):

    def setUp(self):

        method_set, _ = MethodSet.objects.get_or_create(**methodset_example)

        Method.objects.create(
            id=int(method.attrib['id'].split('id')[-1]),
            method_set=method_set,
            name=find_tag_text(method, 'name'),
            classification=find_tag_text(method, 'classification'),
            raw_notation=find_tag_text(method, 'notation'),
            title=find_tag_text(method, 'title'),
            leadHeadCode=find_tag_text(method, 'leadHead'),
            method_notes=find_tag_text(method, 'notes')
        )
