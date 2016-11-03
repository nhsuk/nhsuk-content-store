import responses
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.test.utils import override_settings
from wagtail.wagtailcore.models import Page, Site

from pages.models import EditorialPage
from pages.preview import PreviewHandler

FRONTEND_PREVIEW_URL = 'http://frontend/preview'


class PreviewHandlerTestCase(TestCase):
    def setUp(self):
        super(PreviewHandlerTestCase, self).setUp()

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

    @override_settings(FRONTEND_PREVIEW_URL='')
    def test_placeholder_returned_with_empty_settings(self):
        """
        Tests that if `settings.FRONTEND_PREVIEW_URL` is empty,
        the preview handler returns a placeholder string.
        """

        handler = PreviewHandler()
        self.assertEqual(
            handler.get_html_preview(self.request, self.page),
            '<p>Preview page not configured.</p>'
        )

    @responses.activate
    @override_settings(FRONTEND_PREVIEW_URL=FRONTEND_PREVIEW_URL)
    def test_preview_html(self):
        """
        Tests that if `settings.FRONTEND_PREVIEW_URL` is set,
        the preview handler makes a post with the API json of
        the page.
        """
        expected_html = '<html><strong>Preview ...</strong></html>'
        responses.add(
            responses.POST, FRONTEND_PREVIEW_URL,
            body=expected_html, status=200
        )

        handler = PreviewHandler()
        self.assertEqual(
            handler.get_html_preview(self.request, self.page),
            expected_html
        )

    @responses.activate
    @override_settings(FRONTEND_PREVIEW_URL=FRONTEND_PREVIEW_URL)
    def test_relative_urls_tranformed_into_absolute(self):
        """
        Tests that all the relative urls in the html of the preview
        page are tranformed into absolute ones.
        """
        raw_html = """
<html>
    <body>
        <a href="/should-become-absolute"/>
        <a href="http://should-stay-the-same"/>
        <a/>
        <link href="/should-become-absolute"/>
        <link href="http://should-stay-the-same"/>
        <link/>
        <img src="/should-become-absolute"/>
        <img src="http://should-stay-the-same"/>
        <img/>
        <img srcset="/should-become-absolute,/should-become-absolute"/>
        <img srcset="http://should-stay-the-same,http://should-stay-the-same"/>
    </body>
</html>
"""
        expected_html = """
<html>
    <body>
        <a href="http://frontend/should-become-absolute"/>
        <a href="http://should-stay-the-same"/>
        <a/>
        <link href="http://frontend/should-become-absolute"/>
        <link href="http://should-stay-the-same"/>
        <link/>
        <img src="http://frontend/should-become-absolute"/>
        <img src="http://should-stay-the-same"/>
        <img/>
        <img srcset="http://frontend/should-become-absolute,http://frontend/should-become-absolute"/>
        <img srcset="http://should-stay-the-same,http://should-stay-the-same"/>
    </body>
</html>
"""
        responses.add(
            responses.POST, FRONTEND_PREVIEW_URL,
            body=raw_html, status=200
        )

        handler = PreviewHandler()
        self.assertEqual(
            handler.get_html_preview(self.request, self.page).strip(),
            expected_html.strip()
        )
