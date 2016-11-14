#!/usr/bin/env python
# coding=utf-8

"""MDMultiSelect module."""

from django.forms import SelectMultiple
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .mdselect import MDSelect


class MDMultiSelect(MDSelect, SelectMultiple):

    """MDSelect widget that allows multiple select."""

    allow_multiple_selected = True

    def render(self, name, value, attrs=None):
        """Render the widget."""
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name, **{
            "data-multiple": True
        })
        output = [format_html('<md-select{}>', flatatt(final_attrs))]
        options = self.render_options(value)
        if options:
            output.append(options)
        output.append('</md-select>')
        return mark_safe('\n'.join(output))
