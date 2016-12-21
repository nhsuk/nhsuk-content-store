import logging
import os

from bakery.views import BuildableMixin

from images.models import Image

logger = logging.getLogger(__name__)


class BakeryImageView(BuildableMixin):
    specs = [
        'width-300',
        'width-400',
        'width-600',
        'width-800',
        'width-1280',
    ]

    def __init__(self, build_path):
        super(BakeryImageView, self).__init__()
        self.build_path = build_path

    @property
    def build_method(self):
        for image in Image.objects.all():
            self.build_object(image)

    def build_object(self, obj):
        logger.debug("Building %s" % obj)

        for spec in self.specs:
            rendition = obj.get_rendition(spec)
            rendition.file.open('rb')

            path = self.get_build_path(obj, spec)
            self.build_file(path, rendition)

    def get_build_path(self, obj, spec):
        path = os.path.join(self.build_path, 'images')
        os.path.exists(path) or os.makedirs(path)
        name = '{}-{}'.format(spec, obj.slug)
        return os.path.join(path, name)

    def build_file(self, path, rendition):
        with open(path, 'wb+') as destination:
            for chunk in rendition.file.chunks():
                destination.write(chunk)
