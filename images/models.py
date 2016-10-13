from django.db import models
from wagtail.wagtailimages.models import Image as WagtailImage


class Image(WagtailImage):
    caption = models.CharField(
        max_length=255, blank=True,
        help_text='Optional. It will be displayed below the image.'
    )
    alt = models.CharField(
        max_length=255, blank=True,
        help_text='Optional. Alternate text for an image, if the image cannot be displayed.'
    )

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'caption',
        'alt',
        'tags',
        'focal_point_x',
        'focal_point_y',
        'focal_point_width',
        'focal_point_height',
    )

    api_fields = [
        'title', 'caption', 'alt', 'width', 'height'
    ]
