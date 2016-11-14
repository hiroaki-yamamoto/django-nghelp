#!/usr/bin/env python
# coding=utf-8

"""MDSelect widgets."""

from django.forms import Select
from django.forms.utils import flatatt
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class MDSelect(Select):

    """MDSelect."""

    def __init__(self, disable_select=False, *args, **kwargs):
        """Init the class."""
        super(MDSelect, self).__init__(*args, **kwargs)
        self.disable_select = disable_select

    def render(self, name, value, attrs=None):
        """Render the widget."""
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<md-select{}>', flatatt(final_attrs))]
        options = self.render_options([value])
        if options:
            output.append(options)
        output.append('</md-select>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        """Render the option."""
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices and not self.disable_select:
            selected_html = mark_safe(' data-selected="selected"')
            if not self.allow_multiple_selected:
                # Only allow for a single selection.
                selected_choices.remove(option_value)
        else:
            selected_html = ''
        return format_html('<md-option data-value="{}"{}>{}</md-option>',
                           option_value,
                           selected_html,
                           force_text(option_label))

    def render_options(self, selected_choices):
        """Render option group."""
        # Normalize to strings.
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in self.choices:
            if isinstance(option_label, (list, tuple)):
                output.append(
                    format_html(
                        '<md-optgroup data-label="{}">',
                        force_text(option_value)
                    )
                )
                for option in option_label:
                    output.append(
                        self.render_option(selected_choices, *option)
                    )
                output.append('</md-optgroup>')
            else:
                output.append(self.render_option(
                    selected_choices, option_value, option_label
                ))
        return '\n'.join(output)
