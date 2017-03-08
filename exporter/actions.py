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

from .components import StructuralComponent

logger = logging.getLogger(__name__)


class BakeryPageView(BuildableMixin):
    CONTENT_AREAS = ['header', 'main']

    def __init__(self, build_path):
        super().__init__()
        self.build_path = build_path

    def transform_content(self, obj, raw_content):
        """
        Transforms the content returned by the API into something that the frontend expects.
        This is because there are some differences between the frontend REST handler and the filesystem one
        (e.g. images with different formats etc.)
        """
        content = json.loads(raw_content.decode('utf-8'))
        context = {
            'page': obj,
            'root_path': self.build_path,
            'item_base_path': self.get_item_base_path(obj),
            'new_files': []
        }

        component_exporter = StructuralComponent(context)
        for area in self.CONTENT_AREAS:
            content_area = content.get('content', {}).get(area, [])
            if content_area:
                content['content'][area] = component_exporter.transform_components(content_area)

        content_files = context['new_files']
        content_files.append(
            (
                os.path.join(context['item_base_path'], 'manifest.json'),
                json.dumps(content, indent=2, sort_keys=True)
            )
        )
        return content_files

    def build_objects(self, ids, include_children=False):
        """
        Exports the live pages with id == `ids` including their children if `include_children` == True.
        """
        for page in Page.objects.live().filter(id__in=ids):
            self.build_object(page, include_children=include_children)

    def build_object(self, obj, include_children=False):
        """
        Exports the live page `obj` including its children if `include_children` == True.
        """
        logger.debug("Building %s" % obj)

        obj = obj.specific

        client = APIClient(SERVER_NAME='localhost')
        client.handler._force_token = self.get_auth_token()
        response = client.get(self.get_url(obj))

        content_files = self.transform_content(obj, response.content)
        for path, content in content_files:
            self.build_file(path, content)

        if include_children:
            for child in obj.get_live_children():
                self.build_object(child, include_children=include_children)

    def build_file(self, path, content, *args, **kargs):
        """
        Saves the `content` in a file with the given `path`.
        """
        folder_path = os.path.dirname(path)
        os.path.exists(folder_path) or os.makedirs(folder_path)

        # if file
        if hasattr(content, 'file'):
            content.file.open('rb')
            with open(path, 'wb+') as destination:
                for chunk in content.file.chunks():
                    destination.write(chunk)
            return

        # if text
        content = content.encode('utf-8')
        return super().build_file(path, content, *args, **kargs)

    def get_url(self, obj):
        """
        Returns the url to the page detail API for the object `obj`.
        """
        return reverse('wagtailapi:pages:detail', kwargs={'pk': obj.pk})

    def get_auth_token(self):
        """
        Instantiate a valid auth token to be used for the request.
        """
        return AccessToken(
            scope='read',
            expires=now() + timedelta(days=1)
        )

    def get_item_base_path(self, obj):
        """
        Returns the path to the folder that will contain the export of the object `obj`.
        It creates those folder if they don't exist.
        """
        path = os.path.join(self.build_path, obj.url[1:])
        os.path.exists(path) or os.makedirs(path)
        return path


def export(build_dir, page_ids):
    """
    Exports the live pages with id == `page_ids` to the folder `build_dir` including their children pages.
    """
    BakeryPageView(build_dir).build_objects(
        page_ids, include_children=True
    )
