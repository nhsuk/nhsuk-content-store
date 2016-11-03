import json
from unittest import mock

import requests
from django.conf import settings
from django.utils.six.moves.urllib.parse import urlparse
from pyquery import PyQuery


class PreviewHandler(object):
    """
    Logic behind the preview logic.
    """
    def __init__(self):
        self.preview_url = settings.FRONTEND_PREVIEW_URL

        if self.preview_url:
            self.preview_base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.preview_url))
        else:
            self.preview_base_url = ''

    def _get_api_representation_of_page(self, request, page):
        """
        Returns the API representation of `page` as a json dict.
        """
        from api.router import api_router

        endpoint = api_router.get_model_endpoint(page.__class__)[1]()
        serializer_class = endpoint._get_serializer_class(api_router, page.__class__, [], show_details=True)
        data = serializer_class(page, context={
            'view': mock.MagicMock(),
            'router': api_router,
            'request': request
        }).data

        return json.dumps(data)

    def _cleanup_html(self, html):
        """
        Cleans the html to return by transforming all the relative URLs to absolute.
        """
        html_data = PyQuery(html)

        for el in html_data('a[href]:not([href^=http]), link[href]:not([href^=http])'):
            el.attrib['href'] = '{}{}'.format(self.preview_base_url, el.attrib['href'])
        for el in html_data('img[src]:not([src^=http]), script[src]:not([src^=http])'):
            el.attrib['src'] = '{}{}'.format(self.preview_base_url, el.attrib['src'])
        for el in html_data('img[srcset]:not([srcset^=http])'):
            srcset = el.attrib['srcset'].split(',')
            el.attrib['srcset'] = ','.join(
                [
                    '{}{}'.format(self.preview_base_url, src.strip())
                    for src in srcset
                ]
            )

        return html_data.outer_html()

    def _build_html_preview(self, api_data):
        """
        Returns the untouched HTML of the preview page by:
            - posting the page data to a given url
            - have that url use that data to render the page

        If the preview url settings is not set, a simple placeholder string is returned.
        """
        if self.preview_url:
            response = requests.post(self.preview_url, data={
                'page': api_data
            })
            return response.content

        return 'Preview page not configured.'

    def get_html_preview(self, request, page):
        """
        Returns the HTML of the preview page `page`.
        """
        api_data = self._get_api_representation_of_page(request, page)
        html = self._build_html_preview(api_data)
        return self._cleanup_html(html)
