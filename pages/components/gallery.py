from wagtail.wagtailcore.blocks import ChoiceBlock, StructBlock

from ..blocks import StreamBlock
from .base import Component
from .image import image


class GalleryBlock(StructBlock):
    variant = ChoiceBlock(
        label='Variant',
        choices=(
            ('inline', 'Inline'),
            ('collage', 'Collage'),
        )
    )

    children = StreamBlock([
        image.as_tuple()
    ], label='Images')


gallery = Component('gallery', GalleryBlock(icon="radio-full"))
