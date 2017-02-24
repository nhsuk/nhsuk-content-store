import logging
from unittest import mock

from django.test import TestCase
from wagtail.wagtailcore.models import Page

from pages.factories import (
    ConditionPageFactory, ConditionsPageFactory, SymptomsPageFactory
)
from pages.models import EditorialPage, FolderPage

from ..actions import Importer


class ImporterTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # prepare db
        ConditionsPageFactory()
        SymptomsPageFactory()

    @mock.patch('importer.actions.get_list_of_children_from_remote')
    @mock.patch('importer.actions.get_data_from_remote')
    def test_import_new_page(self, mocked_get_data_from_remote, mocked_get_list_of_children_from_remote):
        tot_pages = Page.objects.count()

        title = 'test'
        description = 'description'
        mocked_get_list_of_children_from_remote.return_value = []
        mocked_get_data_from_remote.return_value = {
            'layout': 'content-simple',
            'title': title,
            'description': description,
            'choicesOrigin': '',
            'nonEmergencyCallout': True,
            'content': {
                'header': [],
                'main': []
            }
        }
        importer = Importer()

        importer.import_items('conditions', [title])
        self.assertEqual(importer.items_in_error, [])

        self.assertEqual(Page.objects.count(), tot_pages + 1)
        page = EditorialPage.objects.get(slug='test')

        self.assertEqual(page.title, title)
        self.assertEqual(page.choices_origin, '')
        self.assertEqual(page.search_description, description)
        self.assertEqual(page.non_emergency_callout, True)
        self.assertTrue(page.live)

    @mock.patch('importer.actions.get_list_of_children_from_remote')
    @mock.patch('importer.actions.get_data_from_remote')
    def test_import_existing_page(self, mocked_get_data_from_remote, mocked_get_list_of_children_from_remote):
        title = 'test'
        description = 'description'
        ConditionPageFactory(title=title, slug=title, search_description='old text')

        tot_pages = Page.objects.count()

        mocked_get_list_of_children_from_remote.return_value = []
        mocked_get_data_from_remote.return_value = {
            'layout': 'content-simple',
            'title': title,
            'choicesOrigin': '',
            'description': description,
            'nonEmergencyCallout': True,
            'content': {
                'header': [],
                'main': []
            }
        }
        importer = Importer()

        importer.import_items('conditions', [title])
        self.assertEqual(importer.items_in_error, [])

        self.assertEqual(Page.objects.count(), tot_pages)
        page = EditorialPage.objects.get(slug='test')

        self.assertEqual(page.title, title)
        self.assertEqual(page.choices_origin, '')
        self.assertEqual(page.search_description, description)
        self.assertEqual(page.non_emergency_callout, True)
        self.assertTrue(page.live)

    @mock.patch('importer.actions.get_list_of_children_from_remote')
    @mock.patch('importer.actions.get_data_from_remote')
    def test_import_new_guide(self, mocked_get_data_from_remote, mocked_get_list_of_children_from_remote):
        tot_pages = Page.objects.count()

        mocked_get_list_of_children_from_remote.return_value = []

        folder_page_title = 'folder-test'
        folder_page_description = 'folder description'
        child_page_title = 'test'
        child_page_description = 'child description'

        def mocked_get_data(url_part, *args, **kwargs):
            if url_part.endswith('%s/manifest.json' % folder_page_title):
                return {
                    'layout': 'guide',
                    'title': folder_page_title,
                    'description': folder_page_description,
                    'choicesOrigin': '',
                    'nonEmergencyCallout': True,
                    'meta': {
                        'children': [
                            {'slug': child_page_title}
                        ]
                    }
                }
            return {
                'layout': 'content-simple',
                'title': child_page_title,
                'description': child_page_description,
                'choicesOrigin': '',
                'nonEmergencyCallout': True,
                'content': {
                    'header': [],
                    'main': []
                }
            }

        mocked_get_data_from_remote.side_effect = mocked_get_data
        importer = Importer()

        importer.import_items('conditions', [folder_page_title])
        self.assertEqual(importer.items_in_error, [])

        self.assertEqual(Page.objects.count(), tot_pages + 2)
        folder_page = FolderPage.objects.get(slug=folder_page_title)

        self.assertEqual(folder_page.title, folder_page_title)
        self.assertEqual(folder_page.search_description, folder_page_description)
        self.assertTrue(folder_page.live)

        child_page = folder_page.get_children()[0]
        child_page = child_page.specific
        self.assertEqual(child_page.title, child_page_title)
        self.assertEqual(child_page.search_description, child_page_description)
        self.assertEqual(child_page.choices_origin, '')
        self.assertEqual(child_page.non_emergency_callout, True)
        self.assertTrue(child_page.live)

    @mock.patch('importer.actions.get_list_of_children_from_remote')
    @mock.patch('importer.actions.get_data_from_remote')
    def test_import_new_folder(self, mocked_get_data_from_remote, mocked_get_list_of_children_from_remote):
        tot_pages = Page.objects.count()

        folder_page_title = 'folder-test'
        folder_page_description = 'folder description'
        child_page_title = 'test'
        child_page_description = 'child description'

        # mock get_list_of_children_from_remote
        def mocked_get_list_of_children(url_part):
            is_folder = url_part.endswith(folder_page_title)
            return [child_page_title] if is_folder else []

        mocked_get_list_of_children_from_remote.side_effect = mocked_get_list_of_children

        # mock get_data_from_remote
        def mocked_get_data(url_part, *args, **kwargs):
            is_folder = url_part.endswith('%s/manifest.json' % folder_page_title)
            return {
                'layout': 'content-simple',
                'title': folder_page_title if is_folder else child_page_title,
                'description': folder_page_description if is_folder else child_page_description,
                'choicesOrigin': '',
                'nonEmergencyCallout': True,
                'content': {
                    'header': [],
                    'main': []
                }
            }

        mocked_get_data_from_remote.side_effect = mocked_get_data
        importer = Importer()

        importer.import_items('conditions', [folder_page_title])
        self.assertEqual(importer.items_in_error, [])

        self.assertEqual(Page.objects.count(), tot_pages + 2)
        folder_page = EditorialPage.objects.get(slug=folder_page_title)

        self.assertEqual(folder_page.title, folder_page_title)
        self.assertEqual(folder_page.search_description, folder_page_description)
        self.assertEqual(folder_page.choices_origin, '')
        self.assertEqual(folder_page.non_emergency_callout, True)
        self.assertTrue(folder_page.live)

        child_page = folder_page.get_children()[0]
        child_page = child_page.specific
        self.assertEqual(child_page.title, child_page_title)
        self.assertEqual(child_page.description, child_page_description)
        self.assertEqual(child_page.choices_origin, '')
        self.assertEqual(child_page.non_emergency_callout, True)
        self.assertTrue(child_page.live)

    @mock.patch('importer.actions.get_data_from_remote')
    def test_failing_silently(self, mocked_get_data_from_remote):
        mocked_get_data_from_remote.return_value = {}
        importer = Importer(fail_silently=True)

        logging.disable(logging.CRITICAL)

        importer.import_items('conditions', ['test'])
        self.assertEqual(importer.items_in_error, ['test'])

        logging.disable(logging.NOTSET)

    @mock.patch('importer.actions.get_data_from_remote')
    def test_without_failing_silently(self, mocked_get_data_from_remote):
        mocked_get_data_from_remote.return_value = {}
        importer = Importer(fail_silently=False)

        self.assertRaises(
            KeyError, importer.import_items, 'conditions', ['test']
        )
