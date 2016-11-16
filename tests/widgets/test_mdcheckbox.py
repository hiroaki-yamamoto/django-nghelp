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
        """Test render invokation."""
        result = self.widget.render("result", None)
        data = (
            "<md-checkbox name=\"result\" type=\"checkbox\">"
            "%s</md-checkbox>"
        ) % self.label
        self.assertEqual(result, data)


class MDCheckBoxCheckedTest(TestCase):
    """MDCheckBox Checked test."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", True)
        data = (
            "<md-checkbox checked=\"checked\" name=\"result\" "
            "type=\"checkbox\">%s</md-checkbox>"
        ) % self.label
        self.assertEqual(result, data)


class MDCheckBoxHasClassTest(TestCase):
    """MDCheckBox test in the case that the widget has a value."""

    def setUp(self):
        """Setup."""
        self.label = "This is a test"
        self.widget = MDCheckBox(self.label)

    def test_render(self):
        """Test render invokation."""
        result = self.widget.render("result", "UWAAAAAHHH")
        data = (
            "<md-checkbox checked=\"checked\" name=\"result\" "
            "type=\"checkbox\" value=\"UWAAAAAHHH\">%s</md-checkbox>"
        ) % self.label
        self.assertEqual(result, data)
