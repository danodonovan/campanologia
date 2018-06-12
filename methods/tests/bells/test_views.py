from django.test import Client, TestCase
from django.urls import reverse


class TestBellsViews(TestCase):

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

    def test_home(self):
        response = self.client.get(reverse(viewname='home'))
        self.assertContains(
            response,
            'Bell ringers sometimes need blue lines quickly, this site aims to provide just that.'
        )

    def test_about(self):
        response = self.client.get(reverse(viewname='about'))
        self.assertContains(
            response,
            'This little site has been created as an exercise in web site building, javascript, django and python.'
        )
