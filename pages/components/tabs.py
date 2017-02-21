from wagtail.wagtailcore.blocks import CharBlock, ChoiceBlock

from ..blocks import StreamBlock, StructBlock
from .base import Component
from .image import image


class TabBlock(StructBlock):
    label = CharBlock()
    children = StreamBlock([
        image.as_tuple()
    ], label='Content')


class TabsBlock(StructBlock):
    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('bottom', 'Bottom'),
            ('top', 'Top'),
        )
    )
    children = StreamBlock([
        ('tab', TabBlock())
    ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # delete labels as we don't want them to appear in the admin
        for child_block in self.child_blocks.values():
            child_block.label = None


tabs = Component('tabs', TabsBlock(icon="radio-full"))
