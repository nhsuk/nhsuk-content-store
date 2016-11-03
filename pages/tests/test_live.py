from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.utils import override_settings
from wagtail.wagtailcore.models import Page, Site

from pages.models import EditorialPage

TEST_FRONTEND_BASE_URL = 'https://example.com'


class LivePagesTestCase(TestCase):
    def setUp(self):
        super(LivePagesTestCase, self).setUp()

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
        self.request = self.get_request(self.site)

    def get_request(self, site):
        request = self.client.get('/test/', HTTP_HOST=site.hostname)
        request.site = site
        return request

    @override_settings(FRONTEND_BASE_URL=TEST_FRONTEND_BASE_URL)
    def test_live_page_redirects_to_frontend(self):
        """
        Tests that the url /<page-url>/ redirects to <frontend-url>/<page-url>/ where
            frontend-url == settings.FRONTEND_BASE_URL
        if the page is live
        """
        response = self.client.get(self.page.full_url)
        expected_url = '{}{}'.format(TEST_FRONTEND_BASE_URL, self.page.url)
        self.assertRedirects(response, expected_url, target_status_code=302)

    def test_non_live_page_404s(self):
        """
        Tests that the url /<page-url>/ returns 404 if the page is not live
        """
        self.page.live = False
        self.page.save()

        response = self.client.get(self.page.full_url)
        self.assertEqual(response.status_code, 404)

    def test_non_existing_page_404s(self):
        """
        Tests that if the invalid urls return 404
        """
        invalid_url = '{}invalid/'.format(self.page.full_url)
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    @override_settings(FRONTEND_BASE_URL='')
    def test_placeholder_response_with_empty_settings(self):
        """
        Tests that the url /<page-url>/ returns a placeholder string
        if settings.FRONTEND_BASE_URL has not been set
        """
        response = self.client.get(self.page.full_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Please set FRONTEND_BASE_URL in your settings.py')
