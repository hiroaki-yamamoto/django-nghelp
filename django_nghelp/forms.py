#!/usr/bin/env python
# coding=utf-8

"""Django AngularJS Helper Froms."""

import json
from datetime import date
from functools import wraps
from django import forms


class AngularForm(forms.Form):
    """AngularJS Form."""

    def __wrap_ng_init(self, f, fld):
        """Wrap ng-init attribute."""
        @wraps(f)
        def inside(name, value, attrs):
            format_func = getattr(
                fld, "ng_init_format_func",
                lambda v: (
                    fld.widget.format_value(v)
                    if isinstance(v, (date, str)) else
                    v
                )
            )
            attrs["data-ng-init"] = ("{} = {}").format(
                fld.widget.attrs.get("data-ng-model") or
                attrs["data-ng-model"], json.dumps(format_func(value))
            )
            return f(name, value, attrs)
        return inside

    def __init__(self, *args, **kwargs):
        """Init the function."""
        super(AngularForm, self).__init__(*args, **kwargs)
        metaclass = getattr(self, "Meta", type("Meta", (object,), {}))
        handle_ng_init = getattr(metaclass, "handle_ng_init", False)
        ng_init_format_func = getattr(metaclass, "ng_init_format_func", {})
        self.ng_model_prefix = getattr(metaclass, "ng_model_prefix", "model")

        for (name, field) in self.fields.items():
            model = ("{}.{}").format(self.ng_model_prefix, name)
            field.widget.attrs.setdefault("data-ng-model", model)
            if handle_ng_init:
                if name in ng_init_format_func:
                    setattr(
                        field, "ng_init_format_func",
                        ng_init_format_func[name]
                    )
                tmp = field.widget.get_context
                field.widget.get_context = self.__wrap_ng_init(tmp, field)


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


class FieldAttributeForm(forms.Form):
    """
    Field common attribute form.

    This form enables to specify widget.attrs thru Meta class.

    Example:
    ```Python
    class TestForm(FieldAttributeForm):

        class Meta(object):
            common_attrs = {
                "data-on-load": "test()",
                "data-on-delay": lambda form, fld, name, value: value
            }
            fld_attrs = {
                "name1": {
                    "data-test": "test1"
                },
                "name2": {
                    "data-test": lambda form, fld, name, value: value
                }
            }

        name1 = forms.CharField(required=False)
        name2 = forms.CharField(required=False)
        number = forms.IntegerField(required=False)
    ```

    Above example shows how to handle attributes. Especially, data-on-delay
    and fld_attrs['name2'][data-test] attributes are evaluated when
    widget.get_context is called. Therefore, widget.get_context is wrapped
    to handle metadata attribute.
    """

    def __wrap_attr(self, f, fld):
        """Wrap attribute."""
        @wraps(f)
        def inside(name, value, attrs):
            metaclass = getattr(self, "Meta", type("Meta", (object,), {}))
            attrs.update(getattr(metaclass, "common_attrs", {}))
            attrs.update(getattr(metaclass, "fld_attrs", {}).get(name, {}))
            for (key, value_func) in attrs.items():
                try:
                    attrs[key] = value_func(self, fld, name, value)
                except TypeError:
                    continue
            return f(name, value, attrs)
        return inside

    def __init__(self, *args, **kwargs):
        """Init."""
        super(FieldAttributeForm, self).__init__(*args, **kwargs)
        # print(self.fields)
        for name, fld in self.fields.items():
            tmp = fld.widget.get_context
            fld.widget.get_context = self.__wrap_attr(tmp, fld)
