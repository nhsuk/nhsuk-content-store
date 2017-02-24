import json
import logging

from django.core.exceptions import ObjectDoesNotExist

from pages.models import EditorialPage, FolderPage

from .components import StructuralComponent
from .utils import get_data_from_remote, get_list_of_children_from_remote

logger = logging.getLogger(__name__)


class Importer(object):
    def __init__(self, fail_silently=True):
        self.page_meta = EditorialPage._meta
        self.fail_silently = fail_silently
        self.items_in_error = []

    def get_item_children(self, item_data, item_base_url):
        # if it has a children prop, use that
        if 'children' in item_data.get('meta', {}):
            return [
                child['slug'] for child in item_data['meta']['children']
            ]

        # otherwise, see if there are subfolders
        return get_list_of_children_from_remote(item_base_url)

    def import_item(self, item_slug, item_data, parent_page, item_base_url):
        try:
            is_folder_page = item_data['layout'] == 'guide'
            PageClass = FolderPage if is_folder_page else EditorialPage

            # get page
            try:
                page = PageClass.objects.get(slug__iexact=item_slug)
            except ObjectDoesNotExist:
                page = PageClass()

            # populate basic props
            page.slug = item_slug
            page.title = item_data['title']
            page.search_description = item_data.get('description', '')
            page.live = True

            if is_folder_page:
                page.guide = True
            else:
                page.non_emergency_callout = item_data.get('nonEmergencyCallout', False)
                page.choices_origin = item_data.get('choicesOrigin')

                # populate content fields
                content = item_data['content']
                context = {
                    'item_base_url': item_base_url,
                    'assets_base_url': '',
                    'page': page
                }
                component_importer = StructuralComponent(context)

                transformed_header = component_importer.transform_components(content.get('header', []))
                page.header = self.page_meta.get_field('header').to_python(
                    json.dumps(transformed_header)
                )

                transformed_main = component_importer.transform_components(content['main'])
                page.main = self.page_meta.get_field('main').to_python(
                    json.dumps(transformed_main)
                )

            # save
            if page.pk:
                page.save()
            else:
                parent_page.add_child(instance=page)
            page.save_revision()

            # do the same with children
            children = self.get_item_children(item_data, item_base_url)
            if children:
                self._import_items(children, page, item_base_url)
        except Exception as e:
            if self.fail_silently:
                logger.exception(e)
                self.items_in_error.append(item_slug)
            else:
                raise e

    def _import_items(self, items, parent_page, content_base_url):
        for item_slug in items:
            logger.debug('importing %s' % item_slug)

            item_base_url = '%s/%s' % (content_base_url, item_slug)
            data = get_data_from_remote('%s/manifest.json' % item_base_url, is_json=True)

            self.import_item(item_slug, data, parent_page, item_base_url)

    def import_items(self, item_type, items):
        parent_page = FolderPage.objects.get(slug=item_type)
        content_base_url = '/content/%s' % item_type
        self._import_items(items, parent_page, content_base_url)
