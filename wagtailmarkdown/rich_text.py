import json

from django.forms import widgets
from wagtail.utils.widgets import WidgetWithScript
from wagtail.wagtailadmin.edit_handlers import RichTextFieldPanel


class SimpleMDETextArea(WidgetWithScript, widgets.Textarea):
    """
    SimpleMDE widget for Markdown text.

    Usage:

        To use SimpleMDE for all RichTextField and RichTextBlock instances:

            # settings.py
            WAGTAILADMIN_RICH_TEXT_EDITORS = {
                'default': {
                    'WIDGET': 'wagtailmarkdown.rich_text.SimpleMDETextArea'
                },
            }

            # models.py
            md_field = RichTextField(...)
            stream_field = StreamField([('md', RichTextBlock(...)), ...])

        Or, to use SimpleMDE for certain instances...

            # settings.py
            WAGTAILADMIN_RICH_TEXT_EDITORS = {
                'default': {
                    'WIDGET': 'wagtail.wagtailadmin.rich_text.HalloRichTextArea'
                },
                'simpleMDE': {
                    'WIDGET': 'wagtailmarkdown.rich_text.SimpleMDETextArea'
                },
            }

            # models.py
            md_field = RichTextField(editor='simpleMDE', ...)
            stream_field = StreamField([('md', RichTextBlock(editor='simpleMDE', ...)), ...])

    """

    @classmethod
    def getDefaultArgs(cls):
        return {
            'forceSync': True,
            'spellChecker': True,
            'hideIcons': ['image']
        }

    def __init__(self, attrs=None, **kwargs):
        super().__init__(attrs)
        self.options = dict(self.getDefaultArgs())
        self.options.update(kwargs.get('options', {}))

    def get_panel(self):
        return RichTextFieldPanel

    def render_js_init(self, id_, name, value):
        return "initSimpleMDE({0}, {1});".format(json.dumps(id_), json.dumps(self.options))
