from django.test import TestCase
from wagtail.wagtailcore.models import Collection
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.tests.utils import get_test_image_file


class BaseImageTestCase(TestCase):
    def setUp(self):
        super(BaseImageTestCase, self).setUp()

        Collection.objects.create(
            name="Root",
            path='0001',
            depth=1,
            numchild=0,
        )


class ImageSlugTestCase(BaseImageTestCase):
    def test_create(self):
        image = get_image_model().objects.create(
            title="Test image",
            file=get_test_image_file()
        )
        self.assertEqual(
            image.slug, 'test-image.png'
        )

    def test_update(self):
        image = get_image_model().objects.create(
            title="Test image",
            file=get_test_image_file()
        )

        image.title = 'Something else'
        image.save()

        self.assertEqual(
            image.slug, 'something-else.png'
        )

    def test_very_long_title(self):
        image = get_image_model().objects.create(
            title="a" * 255,
            file=get_test_image_file()
        )

        self.assertEqual(
            image.slug, '{}.png'.format('a' * 50)
        )

    def test_dots_in_title(self):
        image = get_image_model().objects.create(
            title="a.b.c",
            file=get_test_image_file()
        )

        self.assertEqual(
            image.slug, 'ab.png'
        )


class ImageVersionTestCase(BaseImageTestCase):
    def test_create_defaults_to_1(self):
        image = get_image_model().objects.create(
            title="Test image",
            file=get_test_image_file()
        )
        self.assertEqual(image.version, 1)

    def test_update(self):
        image = get_image_model().objects.create(
            title="Test image",
            file=get_test_image_file()
        )

        image.save()
        self.assertEqual(image.version, 2)

        image.save()
        self.assertEqual(image.version, 3)
