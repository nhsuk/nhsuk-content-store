import imghdr

from django.db import models
from django.utils.text import slugify
from wagtail.wagtailimages.models import Image as WagtailImage


class Image(WagtailImage):
    caption = models.CharField(
        max_length=255, blank=True,
        help_text='Optional. It will be displayed below the image.'
    )
    slug = models.SlugField(
        allow_unicode=True,
        max_length=255
    )
    version = models.IntegerField(default=1)

    admin_form_fields = (
        'title',
        'file',
        'collection',
        'caption',
        'tags',
        'focal_point_x',
        'focal_point_y',
        'focal_point_width',
        'focal_point_height',
    )

    api_fields = [
        'title', 'caption', 'slug', 'version', 'width', 'height'
    ]

    def save(self, *args, **kwargs):
        # generate slug
        self.file.open()
        self.slug = '{}.{}'.format(
            slugify(self.title.rsplit('.', 1)[0])[:50],
            (imghdr.what(self.file) or 'jpg')
        )

        # increase version number
        if self.id:
            self.version = self.version + 1

        return super(Image, self).save(*args, **kwargs)
