import logging
import os
from datetime import timedelta

from bakery.views import BuildableMixin
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from oauth2_provider.models import AccessToken
from rest_framework.test import APIClient

from pages.models import Page

logger = logging.getLogger(__name__)


class BakeryPageView(BuildableMixin):
    def __init__(self, build_path):
        super(BakeryPageView, self).__init__()
        self.build_path = build_path

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

        path = self.get_build_path(obj)
        self.build_file(path, response.content)

    def get_url(self, obj):
        return reverse('wagtailapi:pages:detail', kwargs={'pk': obj.pk})

    def get_auth_token(self):
        return AccessToken(
            scope='read',
            expires=now() + timedelta(days=1)
        )

    def get_build_path(self, obj):
        path = os.path.join(self.build_path, obj.url[1:])
        os.path.exists(path) or os.makedirs(path)
        return os.path.join(path, 'manifest.json')
