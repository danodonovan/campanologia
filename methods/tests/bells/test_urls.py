from django.test import Client, TestCase
from django.urls import reverse


class TestBellsUrls(TestCase):

    fixtures = ['methods.json', 'methodset.json', 'firsttowerbellpeal.json']

    @classmethod
    def setUpClass(cls):
        super(TestBellsUrls, cls).setUpClass()
        cls.client = Client()

    def test_home_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_url(self):
        self.assertEqual(reverse(viewname='home'), '/')

    def test_about_status(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 301)

    def test_about_url(self):
        self.assertEqual(reverse(viewname='about'), '/about/')

    def test_methods_status(self):
        response = self.client.get('/methods')
        self.assertEqual(response.status_code, 301)

    def test_search_status(self):
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

    def test_sitemap_url(self):
        self.assertEqual(reverse(viewname='sitemap_url'), '/sitemap.xml')

    def test_sitemap_methodsets(self):
        response = self.client.get('/sitemap-method_sets.xml')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_methodsets_url(self):
        self.assertEqual(
            reverse(viewname='sitemaps', kwargs=dict(section='method_sets')),
            '/sitemap-method_sets.xml'
        )

    def test_sitemap_methods(self):
        response = self.client.get('/sitemap-methods.xml')
        self.assertEqual(response.status_code, 200)

    def test_sitemap_methods_url(self):
        self.assertEqual(
            reverse(viewname='sitemaps', kwargs=dict(section='methods')),
            '/sitemap-methods.xml'
        )
