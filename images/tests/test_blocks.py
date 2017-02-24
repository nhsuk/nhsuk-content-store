from unittest import mock

from django.test import TestCase
from wagtail.wagtailcore.models import Collection
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file

from images.blocks import ImageChooserBlock


class ImageChooserBlockTestCase(TestCase):
    def setUp(self):
        super().setUp()

        Collection.objects.create(
            name="Root",
            path='0001',
            depth=1,
            numchild=0,
        )

        self.image = get_image_model().objects.create(
            title="Test image",
            file=get_test_image_file()
        )

    def get_mocked_router(self, expected_data):
        mocked_endpoint = mock.MagicMock()
        mocked_endpoint.return_value = mock.MagicMock()
        mocked_endpoint()._get_serializer_class()().data = expected_data

        mocked_router = mock.MagicMock()
        mocked_router.get_model_endpoint.return_value = ['images', mocked_endpoint]
        return mocked_router

    def test_empty_list(self):
        block = ImageChooserBlock()

        representation = block.to_api_representation(None, context={'key': 'value'})
        self.assertEqual(representation, None)

    def test_empty_context(self):
        block = ImageChooserBlock()

        representation = block.to_api_representation(self.image, context={})
        self.assertEqual(representation, None)

    def test_value(self):
        block = ImageChooserBlock()

        expected_data = {
            'id': self.image.id,
            'title': self.image.title,
            'width': self.image.width,
            'height': self.image.height,
            'alt': self.image.title,
            'version': 1,
            'caption': self.image.caption,
            'slug': self.image.slug
        }
        mocked_router = self.get_mocked_router(expected_data)

        representation = block.to_api_representation(
            self.image, context={
                'request': mock.MagicMock(),
                'router': mocked_router,
                'view': mock.MagicMock()
            }
        )

        for key, value in expected_data.items():
            self.assertEqual(representation[key], value)
