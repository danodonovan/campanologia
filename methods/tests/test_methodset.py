from django.test import TestCase

from methods.models import MethodSet


methodset_example = dict(
    notes="<notes>",
    p_stage=1,
    p_lengthOfLead=1,
    p_numberOfHunts=1,
    p_huntBellPath="<huntbellPath>",
    p_symmetry="<symmetry>"
)


class MethodSetTestCase(TestCase):

    def setUp(self):
        MethodSet.objects.create(**methodset_example)

    def test_set_correctly(self):
        method_set = MethodSet.objects.get(notes="<notes>")
        self.assertEqual(method_set.notes, "<notes>")
        self.assertEqual(method_set.p_stage, 1)
        self.assertEqual(method_set.p_lengthOfLead, 1)
        self.assertEqual(method_set.p_numberOfHunts, 1)
        self.assertEqual(method_set.p_huntBellPath, "<huntbellPath>")
        self.assertEqual(method_set.p_symmetry, "<symmetry>")

    def test_get_nchanges(self):
        method_set = MethodSet.objects.get(notes="<notes>")
        self.assertEqual(method_set.get_nchanges(), 0)

    def test_get_absolute_url_is_correct(self):
        method_set = MethodSet.objects.get(notes="<notes>")
        self.assertEqual(method_set.get_absolute_url(), "/methods/sets/notes/")

    def test_get_unique_hash(self):
        method_set = MethodSet.objects.get(notes="<notes>")
        self.assertEqual(method_set.get_unique_hash(), "2a787df7dff72613c385ae4831d7cfd8635d4b9c7b988ab91e627021")

    def test_save_overridden(self):
        method_set = MethodSet.objects.get(notes="<notes>")
        self.assertEqual(method_set.slug, "notes")
        self.assertEqual(method_set.uniq_hash, "2a787df7dff72613c385ae4831d7cfd8635d4b9c7b988ab91e627021")
