from wagtail.wagtailcore.blocks import CharBlock, ChoiceBlock

from ..blocks import StreamBlock, StructBlock
from .base import Component
from .gallery import gallery
from .text import text


class RevealBlock(StructBlock):
    summary = CharBlock()

    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('inline', 'Inline'),
            ('block', 'Block'),
        )
    )

    children = StreamBlock([
        text.as_tuple(),
        gallery.as_tuple()
    ], label='Content')


reveal = Component('reveal', RevealBlock(icon="radio-full"))
