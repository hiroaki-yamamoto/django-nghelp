#!/usr/bin/env python
# coding=utf-8

"""Forms Test."""

from django import forms, setup
from django.test import TestCase
from django_nghelp.forms import AngularForm, AllRequiredForm

setup()


class SimpleAngularFormInitTest(TestCase):
    """Simply AngularJS Initialization test."""

    def setUp(self):
        """Setup."""
        class AngularExampleForm(AngularForm):
            """Example form for AngularJS."""

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = AngularExampleForm

    def test_form(self):
        """All form field should have proper value at data-ng-model."""
        result = self.form_cls()
        for (name, field) in result.fields.items():
            self.assertTrue(
                set({"data-ng-model": "model.%s" % name}.items()).issubset(
                    set(field.widget.attrs.items())
                ),
                (
                    "Field %s doesn't have data-ng-model attribute"
                    " with proper value."
                ) % name
            )


class CustomModelAngularFormInitTest(TestCase):
    """AngularJS Initialization test on custom model prefix."""

    def setUp(self):
        """Setup."""
        class AngularExampleForm(AngularForm):
            """Example form for AngularJS."""

            ng_model_prefix = "pwn"
            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = AngularExampleForm

    def test_form(self):
        """All form field should have proper value at data-ng-model."""
        result = self.form_cls()
        for (name, field) in result.fields.items():
            self.assertTrue(
                set({
                    "data-ng-model": "%s.%s" % (
                        self.form_cls.ng_model_prefix, name
                    )
                }.items()).issubset(set(field.widget.attrs.items())),
                (
                    "Field %s doesn't have data-ng-model attribute"
                    " with proper value."
                ) % name
            )


class AllRequiredFormSimpleTest(TestCase):
    """All required form simple initialization test."""

    def setUp(self):
        """Setup."""
        class TestForm(AllRequiredForm):
            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = TestForm

    def test_form(self):
        """The form should have required=True attr."""
        result = self.form_cls()
        for (name, fld) in result.fields.items():
            self.assertTrue(
                fld.required, "required flag of %s is Falsy" % name
            )


class AllRequiredFormExceptionTest(TestCase):
    """All required form initialization test with some exception."""

    def setUp(self):
        """Setup."""
        class TestForm(AllRequiredForm):
            class Meta(object):
                optional = ("name2", "name3")

            name1 = forms.CharField(required=False)
            name2 = forms.CharField(required=False)
            name3 = forms.CharField(required=False)
            number = forms.IntegerField(required=False)
        self.form_cls = TestForm

    def test_optional(self):
        """Any attrs that are in optional metadata shouldn't be required."""
        result = self.form_cls()
        for name in self.form_cls.Meta.optional:
            self.assertFalse(
                result.fields[name].required,
                "required flag of %s is Truthy" % name
            )

    def test_required(self):
        """Any attrs that aren't in optional metadata shouldn't be required."""
        result = self.form_cls()
        names = set(result.fields.keys()) - set(self.form_cls.Meta.optional)
        for name in names:
            self.assertTrue(
                result.fields[name].required,
                "required flag of %s is Falsy" % name
            )
