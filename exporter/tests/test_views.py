import json
import tempfile
import zipfile

from django.core.urlresolvers import reverse
from django.test import TestCase
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Collection, Page, Site
from wagtail.wagtailimages.tests.utils import Image, get_test_image_file

from pages.factories import ConditionPageFactory
from pages.models import EditorialPage


class ExportContentTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        # Set up pages
        ConditionPageFactory(
            title='condition-1', slug='condition-1',
            main=EditorialPage._meta.get_field('main').to_python(
                json.dumps([{
                    'type': 'text',
                    'value': {
                        'variant': 'markdown',
                        'value': 'lorem ipsum'
                    }
                }])
            )
        )
        self.site = Site.objects.create(
            hostname='localhost',
            root_page=Page.objects.get(slug='root'),
            is_default_site=True
        )

        # set up images
        Collection.objects.create(
            name="Root",
            path='0001',
            depth=1,
            numchild=0,
        )

        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(),
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
                self.assertCountEqual(
                    zf.namelist(),
                    [
                        'content/home/manifest.json',
                        'content/home/conditions/manifest.json',
                        'content/home/conditions/condition-1/manifest.json',
                        'content/home/conditions/condition-1/content-1.md',
                        'content/images/width-1280-test-image.png',
                        'content/images/width-300-test-image.png',
                        'content/images/width-400-test-image.png',
                        'content/images/width-600-test-image.png',
                        'content/images/width-800-test-image.png',
                    ]
                )

    def test_redirects_to_login_if_not_logged_in(self):
        self.client.logout()

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + self.url)
