import tempfile
import zipfile

from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.test import TestCase
from wagtail.tests.utils import WagtailTestUtils
from wagtail.wagtailcore.models import Collection, Page, Site
from wagtail.wagtailimages.tests.utils import Image, get_test_image_file

from pages.models import EditorialPage


class ExportContentTestCase(TestCase, WagtailTestUtils):
    def setUp(self):
        # set up pages
        root = Page.objects.create(
            title="Root",
            slug='root',
            content_type=ContentType.objects.get_for_model(Page),
            path='0001',
            depth=1,
            numchild=1,
            url_path='/',
        )
        self.site = Site.objects.create(hostname='localhost', root_page=root, is_default_site=True)

        self.page = EditorialPage.objects.create(
            title="Page",
            slug='page',
            content_type=ContentType.objects.get_for_model(EditorialPage),
            path='00010001',
            depth=2,
            numchild=0,
            url_path='/page/',
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
                        'content/images/width-1280-test-image.png',
                        'content/images/width-300-test-image.png',
                        'content/images/width-400-test-image.png',
                        'content/images/width-600-test-image.png',
                        'content/images/width-800-test-image.png',
                        'content/page/manifest.json'
                    ]
                )

    def test_redirects_to_login_if_not_logged_in(self):
        self.client.logout()

        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('wagtailadmin_login') + '?next=' + self.url)
