from unittest import skip

from django.test import Client, TestCase
from django.urls import reverse


class TestMethodsUrls(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMethodsUrls, cls).setUpClass()
        cls.client = Client()

    def test_order_status(self):
        response = self.client.get('/methods/order/6')
        self.assertEqual(response.status_code, 200)

    def test_order_url(self):
        self.assertEqual(
            reverse(viewname='methods:order', kwargs=dict(order=6)),
            '/methods/order/6'
        )

    def test_order_paginated_status(self):
        response = self.client.get('/methods/order/6/1/')
        self.assertEqual(response.status_code, 200)

    def test_order_paginated_url(self):
        self.assertEqual(
            reverse(viewname='methods:order_paginated', kwargs=dict(order=6, page=1)),
            '/methods/order/6/1/'
        )

    def test_list_method_set_status(self):
        response = self.client.get('/methods/sets/single-hunt-minimus-methods/')
        self.assertEqual(response.status_code, 200)

    def test_list_method_set_url(self):
        self.assertEqual(
            reverse(viewname='methods:list_method_set', kwargs=dict(slug='single-hunt-minimus-methods')),
            '/methods/sets/single-hunt-minimus-methods/'
        )

    def test_random_status(self):
        response = self.client.get('/methods/random/')
        self.assertEqual(response.status_code, 200)

    def test_random_url(self):
        self.assertEqual(
            reverse(viewname='methods:random'),
            '/methods/random/'
        )

    @skip('Will not pass if DB not set up')
    def test_single_method_status(self):
        response = self.client.get('/methods/plain-bob-minimus/')
        self.assertEqual(response.status_code, 200)

    def test_single_method_url(self):
        self.assertEqual(
            reverse(viewname='methods:single_method', kwargs=dict(slug='plain-bob-minimus')),
            '/methods/plain-bob-minimus/'
        )

    @skip('Will not pass if DB not set up')
    def test_detail_method_status(self):
        response = self.client.get('/methods/plain-bob-minimus/details')
        self.assertEqual(response.status_code, 200)

    def test_detail_method_url(self):
        self.assertEqual(
            reverse(viewname='methods:detail_method', kwargs=dict(slug='plain-bob-minimus')),
            '/methods/plain-bob-minimus/details'
        )

    def test_search_redirect_status(self):
        response = self.client.get('/methods/')
        self.assertEqual(response.status_code, 302)

    def test_search_redirect_url(self):
        self.assertEqual(
            reverse(viewname='methods:search_redirect'),
            '/methods/'
        )
