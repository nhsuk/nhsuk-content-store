import imghdr

from django.db import models
from django.utils.crypto import get_random_string
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

    @property
    def alt(self):
        return self.title

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
        'alt', 'caption', 'slug', 'version', 'width', 'height'
    ]

    def save(self, *args, **kwargs):
        # generate slug
        self._random_slug_postfix = get_random_string(4)
        self.file.open()
        self.slug = '{}-{}.{}'.format(
            slugify(self.title.rsplit('.', 1)[0])[:50],
            self._random_slug_postfix,
            (imghdr.what(self.file) or 'jpg')
        )

        # increase version number
        if self.id:
            self.version = self.version + 1

        return super().save(*args, **kwargs)
