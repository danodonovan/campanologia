#!/usr/bin/env python
# encoding: utf-8
from django.test import TestCase

from methods.notation import _lead_head


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
