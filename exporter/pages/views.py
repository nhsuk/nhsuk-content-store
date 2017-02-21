import json
import logging
import os
from datetime import timedelta

from bakery.views import BuildableMixin
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from oauth2_provider.models import AccessToken
from rest_framework.test import APIClient

from pages.models import Page

from ..components import StructuralComponent

logger = logging.getLogger(__name__)


class BakeryPageView(BuildableMixin):
    CONTENT_AREAS = ['header', 'main']

    def __init__(self, build_path):
        super(BakeryPageView, self).__init__()
        self.build_path = build_path

    def transform_content(self, obj, raw_content):
        content = json.loads(raw_content.decode('utf-8'))
        context = {
            'item_base_path': self.get_item_base_path(obj),
            'new_files': []
        }

        component_exporter = StructuralComponent(context)
        for area in self.CONTENT_AREAS:
            content_area = content.get('content', {}).get(area, [])
            if content_area:
                component_exporter.transform_components(content_area)

        content_files = context['new_files']
        content_files.append(
            (
                os.path.join(context['item_base_path'], 'manifest.json'),
                json.dumps(content, indent=2, sort_keys=True)
            )
        )
        return content_files

    @property
    def build_method(self):
        for page in Page.objects.exclude(slug='root').live():
            self.build_object(page)

    def build_object(self, obj):
        logger.debug("Building %s" % obj)

        obj = obj.specific

        client = APIClient(SERVER_NAME='localhost')
        client.handler._force_token = self.get_auth_token()
        response = client.get(self.get_url(obj))

        content_files = self.transform_content(obj, response.content)
        for path, content in content_files:
            self.build_file(path, content.encode('utf-8'))

    def get_url(self, obj):
        return reverse('wagtailapi:pages:detail', kwargs={'pk': obj.pk})

    def get_auth_token(self):
        return AccessToken(
            scope='read',
            expires=now() + timedelta(days=1)
        )

    def get_item_base_path(self, obj):
        path = os.path.join(self.build_path, obj.url[1:])
        os.path.exists(path) or os.makedirs(path)
        return path
