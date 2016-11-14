#!/usr/bin/env python
# coding=utf-8

"""Datepicker for Django."""

from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class MDDatePicker(forms.DateInput):

    """AngularJS Material DatePicker for Django."""

    input_type = "date"

    def render(self, name, value, attrs=None):
        """Render the widget."""
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(self._format_value(value))
        return format_html(
            "<md-datepicker{}></md-datepicker>", flatatt(final_attrs)
        )
