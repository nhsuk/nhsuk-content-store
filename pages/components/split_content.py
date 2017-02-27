from wagtail.wagtailcore.blocks import StructBlock

from ..blocks import StreamBlock
from .base import Component
from .reveal import reveal
from .text import text


class SplitAreaBlock(StructBlock):
    children = StreamBlock([
        text.as_tuple(),
        reveal.as_tuple()
    ])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # delete labels as we don't want them to appear in the admin
        for child_block in self.child_blocks.values():
            child_block.label = None


class SplitContentBlock(StructBlock):
    children = StreamBlock([
        ('splitArea', SplitAreaBlock(label='Split area'))
    ], label='Areas')


split_content = Component('splitContent', SplitContentBlock(label='Split content', icon="radio-full"))
