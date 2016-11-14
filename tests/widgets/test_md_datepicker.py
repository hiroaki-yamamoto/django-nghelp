#!/usr/bin/env python
# coding=utf-8

"""MDDatePicker Test."""

from datetime import datetime
from django import setup
from django.test import TestCase
from django_nghelp.widgets import MDDatePicker


setup()


class SimpleMDDatePickerTest(TestCase):
    """Simple MDDatePicker test."""

    def setUp(self):
        """Setup."""
        self.widget = MDDatePicker()

    def test_render(self):
        """The generated content should be correct."""
        result = str(self.widget.render("result", None)).replace("\n", "")
        data = (
            "<md-datepicker name=\"result\" type=\"date\">"
            "</md-datepicker>"
        )
        self.assertEqual(result, data)

    def test_render_has_value(self):
        """The generated content should be correct."""
        now = datetime.utcnow().isoformat()
        result = str(self.widget.render("result", now)).replace("\n", "")
        data = (
            "<md-datepicker name=\"result\" type=\"date\" value=\"{}\">"
            "</md-datepicker>"
        ).format(now)
        self.assertEqual(result, data)
