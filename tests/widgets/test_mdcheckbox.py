#!/usr/bin/env python
# coding=utf-8

"""MDCheckBox Test Case."""


from django import setup
from django.test import TestCase

from django_nghelp.widgets import MDCheckBox


setup()


class SimpleMDCheckBoxTest(TestCase):

    """Simple MDCheckBox Test."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invocation."""
        result = self.widget.render("result", None)
        data = (
            "<md-checkbox name=\"result\" type=\"checkbox\">"
            "%s</md-checkbox>"
        ) % self.label
        self.assertEqual(result, data)
