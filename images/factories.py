import factory
from wagtail.wagtailcore.models import Collection
from wagtail.wagtailimages.tests.utils import get_test_image_file

from . import models


class ImageFactory(factory.django.DjangoModelFactory):
    file = get_test_image_file()

    class Meta:
        model = models.Image

    @classmethod
    def create_collection_if_necessary(cls):
        Collection.objects.get_or_create(
            path='0001',
            defaults={
                'name': 'Root',
                'path': '0001',
                'depth': 1,
                'numchild': 0,
            }
        )

    @classmethod
    def create(cls, *args, **kwargs):
        cls.create_collection_if_necessary()
        return super().create(*args, **kwargs)
