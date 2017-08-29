#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function, division
from io import StringIO
from tempfile import NamedTemporaryFile

from django.core.management import call_command
from django.test import TestCase


_test_xml = u"""
<methodSet>
<notes>Single-hunt Minimus methods</notes>
<properties><stage>4</stage>
<lengthOfLead>8</lengthOfLead>
<numberOfHunts>1</numberOfHunts>
<huntbellPath>1 2 3 4 4 3 2 1</huntbellPath>
<symmetry>palindromic</symmetry></properties>
<method id="id0001">
    <name>Plain</name>
    <classification plain="true">Bob</classification>
    <title>Plain Bob Minimus</title>
    <notation>-14-14,12</notation>
    <leadHeadCode>a</leadHeadCode>
    <performances>
        <firstTowerbellPeal>
            <date>1961-01-21</date>
            <location><town>North Aston</town></location>
        </firstTowerbellPeal>
    </performances>
    <references>
        <rwRef>1961/91</rwRef>
    </references>
</method>
</methodSet>
"""


class Populate(TestCase):

    def test_read_file(self):
        with NamedTemporaryFile('w') as fh:
            fh.write(_test_xml)
            fh.seek(0)
            call_command('populate', '--xml-file', fh.name)
