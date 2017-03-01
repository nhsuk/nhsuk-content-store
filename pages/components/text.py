from django import forms
from wagtail.wagtailcore.blocks import ChoiceBlock, RichTextBlock, StructBlock

from .base import Component

VARIANT_MARKDOWN = 'markdown'
VARIANT_HTML = 'html'
VARIANT_PLAIN = 'plain'

VARIANT_CHOICES = (
    (VARIANT_MARKDOWN, 'Markdown'),
    (VARIANT_HTML, 'HTML'),
    (VARIANT_PLAIN, 'Plain'),
)


class TextBlock(StructBlock):
    variant = ChoiceBlock(
        choices=VARIANT_CHOICES
    )
    value = RichTextBlock()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # delete labels as we don't want them to appear in the admin
        for child_block in self.child_blocks.values():
            child_block.label = None

        # only markdown supported atm so hiding the choices dropdown
        self.child_blocks['variant'].field.widget = forms.HiddenInput()

    class Meta:
        default = {
            'variant': VARIANT_MARKDOWN
        }


text = Component('text', TextBlock(icon="radio-full"))
