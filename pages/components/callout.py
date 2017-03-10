from django.utils.functional import SimpleLazyObject
from wagtail.wagtailcore.blocks import BooleanBlock, ChoiceBlock, StructBlock

from ..blocks import StreamBlock
from .base import Component
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

    def __init__(self, *args, **kwargs):
        children_stream_block = [
            text.as_tuple()
        ]

        # if compact == True, don't allow any other sub-component
        if not kwargs.pop('compact', False):
            # importing components here avoids circular dependency
            from .reveal import reveal_compact

            children_stream_block.append(
                reveal_compact.as_tuple()
            )

        # configure sub-components
        local_blocks = kwargs.get('local_blocks', [])
        local_blocks.append(
            ('children', StreamBlock(children_stream_block, label='Content'))
        )
        kwargs['local_blocks'] = local_blocks

        super().__init__(*args, **kwargs)


callout = SimpleLazyObject(lambda: Component('callout', CalloutBlock(icon="radio-full")))
callout_compact = Component('callout', CalloutBlock(icon="radio-full", compact=True))
