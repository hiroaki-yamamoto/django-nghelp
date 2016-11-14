#!/usr/bin/env python
# coding=utf-8

"""Django AngularJS Helper Froms."""


from django import forms


class AngularForm(forms.Form):

    """AngularJS Form."""

    ng_model_prefix = "model"

    def __init__(self, *args, **kwargs):
        """Init the function."""
        super(AngularForm, self).__init__(*args, **kwargs)
        for (name, field) in self.fields.items():
            model = ("{}.{}").format(self.ng_model_prefix, name)
            field.widget.attrs.setdefault("data-ng-model", model)


class AllRequiredForm(forms.Form):

    """All required form."""

    def __init__(self, *args, **kwargs):
        """Init field."""
        super(AllRequiredForm, self).__init__(*args, **kwargs)
        optional_fields = getattr(
            getattr(self, "Meta", type("Meta", (object,), {})()),
            "optional", None
        ) or {}
        for (name, field) in self.fields.items():
            if name in optional_fields:
                continue
            field.required = True
