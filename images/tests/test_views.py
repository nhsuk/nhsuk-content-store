from django.core.urlresolvers import reverse
from django.test import TestCase
from wagtail.wagtailcore.models import Collection
from wagtail.wagtailimages.tests.utils import Image, get_test_image_file
from wagtail.wagtailimages.views.serve import generate_signature

from images.views import ServeView


class ServeViewTestCase(TestCase):
    def setUp(self):
        Collection.objects.create(
            name="Root",
            path='0001',
            depth=1,
            numchild=0,
        )

        # Create an image for running tests on
        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
        )

    def _get_url(self, signature, image_id, filter_spec, slug, key=ServeView.key):
        return reverse(
            'images_serve',
            args=(signature, image_id, filter_spec, slug)
        )

    def test_success(self):
        # generate signature
        signature = generate_signature(self.image.id, 'fill-800x600', key=ServeView.key)

        # get the image
        url = self._get_url(signature, self.image.id, 'fill-800x600', self.image.slug)
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.streaming)
        self.assertEqual(response['Content-Type'], 'image/png')

    def test_wrong_signature(self):
        # generate wrong signature (different filter spec)
        signature = generate_signature(self.image.id, 'fill-800x700', key=ServeView.key)

        # get the image
        url = self._get_url(signature, self.image.id, 'fill-800x600', self.image.slug)
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 403)

    def test_invalid_filter_spec(self):
        """
        fill-800 is invalid
        """
        # generate signature
        signature = generate_signature(self.image.id, 'fill-800', key=ServeView.key)

        # get the image
        url = self._get_url(signature, self.image.id, 'fill-800', self.image.slug)
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 400)

    def test_wrong_slug(self):
        # generate signature
        signature = generate_signature(self.image.id, 'fill-800x600', key=ServeView.key)

        # get the image
        url = self._get_url(signature, self.image.id, 'fill-800x600', 'invalid-slug')
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 404)

    def test_wrong_id(self):
        # generate signature
        signature = generate_signature(1111111111, 'fill-800x600', key=ServeView.key)

        # get the image
        url = self._get_url(signature, 1111111111, 'fill-800x600', self.image.slug)
        response = self.client.get(url)

        # check response
        self.assertEqual(response.status_code, 404)
