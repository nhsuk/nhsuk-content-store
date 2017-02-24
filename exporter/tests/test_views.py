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

                condition_manifest_path = 'content/home/conditions/condition-1/manifest.json'
                condition_md_path = 'content/home/conditions/condition-1/content-1.md'

                def image_path(slug_postfix, size, in_srcset=False):
                    root = 'assets' if in_srcset else 'content'
                    postfix = ' %sw' % size if in_srcset else ''

                    return '{root}/images/condition-1/test-image-{slug_postfix}-width-{size}.png{postfix}'.format(
                        root=root,
                        slug_postfix=slug_postfix,
                        size=size,
                        postfix=postfix
                    )

                # check manifest.json
                condition_manifest = json.loads(
                    zf.read(condition_manifest_path).decode()
                )
                main_content = condition_manifest['content']['main']
                self.assertEqual(main_content[0]['props']['value'], '!file=content-1.md')
                self.assertCountEqual(
                    main_content[1]['props']['srcset'],
                    [
                        image_path(slug_postfix, 400, in_srcset=True),
                        image_path(slug_postfix, 640, in_srcset=True),
                        image_path(slug_postfix, 800, in_srcset=True),
                        image_path(slug_postfix, 1280, in_srcset=True),
                    ]
                )

                # check md file
                condition_md = zf.read(condition_md_path).decode()
                self.assertEqual(condition_md, 'lorem ipsum')

                # check the zip files
                self.assertCountEqual(
                    zf.namelist(),
                    [
                        condition_manifest_path,
                        condition_md_path,
                        'content/home/manifest.json',
                        'content/home/conditions/manifest.json',
                        image_path(slug_postfix, 400),
                        image_path(slug_postfix, 640),
                        image_path(slug_postfix, 800),
                        image_path(slug_postfix, 1280)
                    ]
                )

    def test_redirects_to_login_if_not_logged_in(self):
        self.client.logout()

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + self.url)
