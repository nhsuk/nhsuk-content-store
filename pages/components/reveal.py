from django.utils.functional import SimpleLazyObject
from wagtail.wagtailcore.blocks import CharBlock, ChoiceBlock, StructBlock

from ..blocks import StreamBlock
from .base import Component
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

    def __init__(self, *args, **kwargs):
        children_stream_block = [
            text.as_tuple()
        ]

        # if compact == True, don't allow any other sub-component
        if not kwargs.pop('compact', False):
            # importing components here avoids circular dependency
            from .callout import callout_compact
            from .gallery import gallery

            children_stream_block += [
                callout_compact.as_tuple(),
                gallery.as_tuple()
            ]

        # configure sub-components
        local_blocks = kwargs.get('local_blocks', [])
        local_blocks.append(
            ('children', StreamBlock(children_stream_block, label='Content'))
        )
        kwargs['local_blocks'] = local_blocks

        super().__init__(*args, **kwargs)


# use a LazyObject for fully defined reveal so that we initialise it only when needed
reveal = SimpleLazyObject(lambda: Component('reveal', RevealBlock(icon="radio-full")))
reveal_compact = Component('reveal', RevealBlock(icon="radio-full", compact=True))
