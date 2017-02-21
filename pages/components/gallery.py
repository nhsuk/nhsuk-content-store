from ..blocks import StreamBlock, StructBlock
from .base import Component
from .image import image


class GalleryBlock(StructBlock):
    children = StreamBlock([
        image.as_tuple()
    ], label='Images')


gallery = Component('gallery', GalleryBlock(icon="radio-full"))
