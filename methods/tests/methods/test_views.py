from django.test import TestCase, Client

from methods.models import MethodSet, Method


class TestSearchView(TestCase):

    fixtures = ['methods.json', 'methodset.json', 'firsttowerbellpeal.json']

    @classmethod
    def setUpClass(cls):
        super(TestSearchView, cls).setUpClass()
        cls.client = Client()

    def test_search_for_plain_bob(self):
        response = self.client.get('/search/?q=plain+bob')
        self.assertContains(response, 'Plain Bob Minimus (4 bells)')


class TestMethodListView(TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMethodListView, cls).setUpClass()
        cls.client = Client()

    def test_methods_title(self):
        response = self.client.get('/methods/order/6')
        self.assertContains(response, '<h1>6 Bell Methods</h1>')

    def test_list_paginates_to_100_methods(self):
        _add_methods(n_methods=101, n_bells=6)
        response = self.client.get('/methods/order/6')
        self.assertContains(response, '<a href="/methods/test-title-100/">')

    def test_list_does_not_paginate_past_100_methods(self):
        _add_methods(n_methods=101, n_bells=6)
        response = self.client.get('/methods/order/6')
        self.assertNotContains(response, '<a href="/methods/test-title-101/">')


def _add_methods(n_methods, n_bells):
    method_set = MethodSet.objects.create(
        id=0,
        notes="<test notes>",
        slug="slug",
        p_stage=n_bells,
        p_lengthOfLead=10,
        p_numberOfHunts=10,
        p_huntBellPath=1,
        p_symmetry="<test symmetry>",
        uniq_hash="<test hash>"
    )
    for i in range(1, n_methods + 1):
        Method.objects.create(
            id=i,
            title='<test title {:03d}>'.format(i),
            slug='slug-{}'.format(i),
            name='<test name {}>'.format(i),
            raw_notation='raw-x{}x'.format(i),
            notation='x{}x'.format(i),
            method_set_id=method_set.id,
        )
