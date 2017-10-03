#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase

from methods.notation import _lead_head, _edge_cases


class LeadHeadTestCase(TestCase):

    def test_not_blank_if_comma_symmetrical(self):

        self.assertEqual(_lead_head("1.1,1"), ("1", "1.1"))

    def test_not_blank_if_comma_odd_bell(self):

        self.assertEqual(_lead_head("1,1.1"), ("1", "1.1"))

    def test_blank_if_no_comma(self):

        self.assertEqual(_lead_head("1.1.1"), ("", "1.1.1"))

    def test_exception_if_more_than_one_comma(self):

        with self.assertRaises(Exception):
            _lead_head("1,1,1")

    def test_exception_if_comma_mid_notation(self):

        with self.assertRaises(Exception):
            _lead_head("1.1,1.1")


class EdgeCasesTestCase(TestCase):

    def test_original(self):

        self.assertEqual(_edge_cases('-1'), ['X', '1'])

    def test_original_odd(self  ):

        for place in ['3', '5', '7', '9', 'E', 'A', 'C']:
            self.assertEqual(_edge_cases(place), ['X', '1'])

    def test_cheeky_little_place(self):

        self.assertEqual(_edge_cases('1'), ['14', '12'])

    def test_exception_if_unknown_edge_case(self):

        with self.assertRaises(Exception):
            _edge_cases('2.2')
