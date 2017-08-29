from django.test import Client, TestCase


class TestBellsUrls(TestCase):

    fixtures = ['methods.json', 'methodset.json', 'firsttowerbellpeal.json']

    @classmethod
    def setUpClass(cls):
        super(TestBellsUrls, cls).setUpClass()
        cls.client = Client()

    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_about(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 301)

    def test_methods(self):
        response = self.client.get('/methods')
        self.assertEqual(response.status_code, 301)

    def test_search(self):
        response = self.client.get('/search')
        self.assertEqual(response.status_code, 301)


class TestSiteMapUrls(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSiteMapUrls, cls).setUpClass()
        cls.client = Client()

    def test_sitemap(self):
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_methodsets(self):
        response = self.client.get('/sitemap-method_sets.xml')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_methods(self):
        response = self.client.get('/sitemap-methods.xml')
        self.assertEqual(response.status_code, 200)
