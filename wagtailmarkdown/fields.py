from django import forms
from django.db import models
from django.utils.encoding import python_2_unicode_compatible, force_text
from django.utils.functional import cached_property

from wagtail.wagtailcore.blocks.field_block import FieldBlock


class MarkdownField(models.TextField):
    def __init__(self, *args, **kwargs):
        self.editor = kwargs.pop('editor', 'default')
        super(MarkdownField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from wagtailmarkdown.wagtailadmin.markdown import get_markdown_editor_widget
        defaults = {'widget': get_markdown_editor_widget(self.editor)}
        defaults.update(kwargs)
        return super(MarkdownField, self).formfield(**defaults)


@python_2_unicode_compatible
class Markdown(object):
    """
    A custom object used to represent a renderable markdown value.
    Provides a 'source' property to access the original source code,
    and renders to the front-end HTML rendering.
    """
    def __init__(self, source):
        self.source = (source or '')

    def __str__(self):
        # this could convert to html for templated front-end. Not needed when using API.
        return self.source

    def __bool__(self):
        return bool(self.source)
    __nonzero__ = __bool__


class MarkdownBlock(FieldBlock):

    def __init__(self, required=True, help_text=None, editor='default', **kwargs):
        self.field_options = {'required': required, 'help_text': help_text}
        self.editor = editor
        super(MarkdownBlock, self).__init__(**kwargs)

    def get_default(self):
        if isinstance(self.meta.default, Markdown):
            return self.meta.default
        else:
            return Markdown(self.meta.default)

    def to_python(self, value):
        return Markdown(value)

    def get_prep_value(self, value):
        return value.source

    @cached_property
    def field(self):
        from wagtailmarkdown.wagtailadmin.markdown import get_markdown_editor_widget
        return forms.CharField(widget=get_markdown_editor_widget(self.editor), **self.field_options)

    def value_for_form(self, value):
        return value.source

    def value_from_form(self, value):
        return Markdown(value)

    def get_searchable_content(self, value):
        return [force_text(value.source)]

    class Meta:
        icon = "doc-full"
