#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, absolute_import

from haystack import indexes
from .models import Method, MethodSet


class MethodIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title')

    def get_model(self):
        return Method

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class MethodSetIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    p_stage = indexes.CharField(model_attr='p_stage')
    notes = indexes.CharField(model_attr='notes')

    def get_model(self):
        return MethodSet

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
