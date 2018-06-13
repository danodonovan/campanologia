from django.test import TestCase, Client


class TestSearchView(TestCase):

    fixtures = ['methods.json', 'methodset.json', 'firsttowerbellpeal.json']

    @classmethod
    def setUpClass(cls):
        super(TestSearchView, cls).setUpClass()
        cls.client = Client()

    def test_search_for_plain_bob(self):
        response = self.client.get('/search/?q=plain+bob')
        self.assertContains(response, 'Plain Bob Minimus (4 bells)')
