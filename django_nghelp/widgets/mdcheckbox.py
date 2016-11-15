#!/usr/bin/env python
# coding=utf-8

"""Selection Btn."""

from django import forms
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html


class MDCheckBox(forms.CheckboxInput):

    """Material Checkbox."""

    def __init__(self, label="", *args, **kwargs):
        """Init the instance."""
        super(MDCheckBox, self).__init__(*args, **kwargs)
        self.label = label

    def render(self, name, value, attrs=None):
        """Render."""
        final_attrs = self.build_attrs(attrs, type='checkbox', name=name)
        label = ""
        if self.check_test(value):
            final_attrs['checked'] = 'checked'
        try:
            label = self.label()
        except TypeError:
            label = self.label
        if not any([isinstance(value, bool), value is None, value == '']):
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_text(value)
        return format_html(
            '<md-checkbox{}>{}</md-checkbox>', flatatt(final_attrs), label
        )
