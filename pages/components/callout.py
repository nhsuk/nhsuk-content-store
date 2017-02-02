from wagtail.wagtailcore.blocks import BooleanBlock, ChoiceBlock

from ..blocks import StreamBlock, StructBlock
from .base import Component
from .reveal import reveal
from .text import text


class CalloutBlock(StructBlock):
    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('info', 'Service control'),
            ('attention', 'Primary care'),
            ('warning', 'Important information'),
            ('alert', 'Urgent care'),
            ('severe', 'Emergency care'),
        )
    )

    compact = BooleanBlock(default=False, required=False)

    children = StreamBlock([
        text.as_tuple(),
        reveal.as_tuple()
    ], label='Content')


callout = Component('callout', CalloutBlock(icon="radio-full"))
