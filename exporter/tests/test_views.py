import json
import tempfile
import zipfile

from django.core.urlresolvers import reverse
from django.test import TestCase
from wagtail.tests.utils import WagtailTestUtils

from images.factories import ImageFactory
from pages.factories import ConditionPageFactory
from pages.models import EditorialPage


class ExportContentTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        # set up images
        self.image = ImageFactory(title='Test image')

        # Set up pages
        ConditionPageFactory(
            title='condition-1', slug='condition-1',
            main=EditorialPage._meta.get_field('main').to_python(
                json.dumps([
                    {
                        'type': 'text',
                        'value': {
                            'variant': 'markdown',
                            'value': 'lorem ipsum'
                        },
                    },
                    {
                        'type': 'image',
                        'value': self.image.pk
                    }
                ])
            )
        )
        self.url = reverse('export-content',)

        # Login
        self.login()

    def test_export(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(self.url)

        with tempfile.NamedTemporaryFile() as tf:
            tf.write(response.content)
            tf.flush()

            with zipfile.ZipFile(tf.name) as zf:
                slug_postfix = self.image._random_slug_postfix
                self.assertCountEqual(
                    zf.namelist(),
                    [
                        'content/home/manifest.json',
                        'content/home/conditions/manifest.json',
                        'content/home/conditions/condition-1/manifest.json',
                        'content/home/conditions/condition-1/content-1.md',
                        'content/images/condition-1/test-image-%s-width-1280.png' % slug_postfix,
                        'content/images/condition-1/test-image-%s-width-800.png' % slug_postfix,
                        'content/images/condition-1/test-image-%s-width-400.png' % slug_postfix,
                        'content/images/condition-1/test-image-%s-width-640.png' % slug_postfix,
                    ]
                )

    def test_redirects_to_login_if_not_logged_in(self):
        self.client.logout()

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + self.url)
