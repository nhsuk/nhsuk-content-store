from wagtail.wagtailcore.blocks import StructBlock

from ..blocks import StreamBlock
from .base import Component
from .image import image


class GalleryBlock(StructBlock):
    children = StreamBlock([
        image.as_tuple()
    ], label='Images')


gallery = Component('gallery', GalleryBlock(icon="radio-full"))
