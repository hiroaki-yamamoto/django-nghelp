#!/usr/bin/env python
# coding=utf-8

"""Selection Btn."""

from django import forms

from .base import BaseWidget


class MDCheckBox(BaseWidget, forms.CheckboxInput):
    """Material Checkbox."""

    template_name = "md_checkbox.html"

    def __init__(self, label="", *args, **kwargs):
        """Init the instance."""
        super(MDCheckBox, self).__init__(*args, **kwargs)
        self.label = label

    def get_context(self, name, value, attrs):
        """Override get_context."""
        ret = super(MDCheckBox, self).get_context(name, value, attrs)
        if "checked" in ret["widget"]["attrs"]:
            ret["widget"]["attrs"]["data-checked"] = \
                ret["widget"]["attrs"].pop("checked")
        ret["widget"]["label"] = self.label
        return ret
