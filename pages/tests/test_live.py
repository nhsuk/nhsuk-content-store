from django.test import TestCase
from django.test.utils import override_settings
from wagtail.wagtailcore.models import Site

from pages.factories import ConditionPageFactory

TEST_FRONTEND_BASE_URL = 'https://example.com'


class LivePagesTestCase(TestCase):
    def setUp(self):
        super().setUp()

        self.page = ConditionPageFactory(title='Page')
        self.request = self.get_request(Site.objects.first())

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
