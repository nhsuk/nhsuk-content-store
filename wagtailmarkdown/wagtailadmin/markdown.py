from __future__ import absolute_import, unicode_literals

import json

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.forms import Media, widgets
from django.utils.module_loading import import_string
from wagtail.utils.widgets import WidgetWithScript

from wagtailmarkdown.edit_handlers import MarkdownFieldPanel


class SimpleMDEArea(WidgetWithScript, widgets.Textarea):
    def get_panel(self):
        return MarkdownFieldPanel

    def render_js_init(self, id_, name, value):
        return "new SimpleMDE({ element: document.getElementById(%s), forceSync: true });" % json.dumps(id_)

    @property
    def media(self):
        return Media(
            js=[
                static('wagtailadmin/js/vendor/simplemde.js'),
            ],
            css={
                'all': [
                    static('wagtailadmin/css/vendor/simplemde.css'),
                ]
            }
        )


DEFAULT_MARKDOWN_EDITORS = {
    'default': {
        'WIDGET': 'wagtailmarkdown.wagtailadmin.markdown.SimpleMDEArea'
    }
}


def get_markdown_editor_widget(name='default'):
    editor_settings = getattr(settings, 'WAGTAILADMIN_MARKDOWN_EDITORS', DEFAULT_MARKDOWN_EDITORS)

    editor = editor_settings[name]
    return import_string(editor['WIDGET'])()
