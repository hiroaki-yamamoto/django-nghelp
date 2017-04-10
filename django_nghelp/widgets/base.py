#!/usr/bin/env python
# coding=utf-8

"""Base classes."""

import os

from django.forms.widgets import Widget
from django.template.backends.jinja2 import Jinja2
from django.utils.safestring import mark_safe


class BaseWidget(Widget):
    """Base widget to render the widget properly."""

    def _render(self, template_name, context, renderer=None):
        """Override render protected function."""
        renderer = renderer or Jinja2({
            'DIRS': [os.path.join(os.path.dirname(__file__), "./jinja2")],
            'APP_DIRS': True,
            'NAME': "django-nghelp-widgets",
            'OPTIONS': {}
        })
        template = renderer.get_template(template_name)
        return mark_safe(template.render(context))
