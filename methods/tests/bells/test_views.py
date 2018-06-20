from django.test import Client, TestCase
from django.urls import reverse


class TestBellsViews(TestCase):

    fixtures = ['methods.json', 'methodset.json', 'firsttowerbellpeal.json']

    @classmethod
    def setUpClass(cls):
        super(TestBellsViews, cls).setUpClass()
        cls.client = Client()

    def test_home_with_debug_set(self):
        with self.settings(DEBUG=True):
            response = self.client.get(reverse(viewname='home'))
            self.assertContains(response, 'Development Site')

    def test_home_without_debug_set(self):
        with self.settings(DEBUG=False):
            response = self.client.get(reverse(viewname='home'))
            self.assertNotContains(response, 'Development Site')
