from unittest import mock

from django.test import TestCase

from pages.factories import ConditionPageFactory, ConditionsPageFactory
from pages.models import EditorialPage

from ..forms import ExportForm


class ExportFormTestCase(TestCase):
    def setUp(self):
        """
        Creates:

        root
            homepage
                conditions (live)
                    level1-a (live)
                    level1-b (draft)
                    level1-c (live)
                        level2-c (live)
        """
        super().setUp()

        ConditionsPageFactory()

        ConditionPageFactory(title='level1-a live', slug='level1-a', live=True)
        ConditionPageFactory(title='level1-b draft', slug='level1-b', live=False)
        level1c = ConditionPageFactory(title='level1-c live', slug='level1-c', live=True)
        ConditionPageFactory(
            title='level2-c live', slug='level2-c', live=True,
            depth=level1c.depth + 1,
            path='{}0001'.format(level1c.path)
        )

    def test_choices_only_show_live_4th_level_pages(self):
        """
        Tests that it should only include:
            level1-a
            level1-b
        """
        form = ExportForm()

        self.assertEqual(
            [choice[1] for choice in form.fields['pages'].choices],
            ['level1-a live', 'level1-c live']
        )

    def test_validation_error(self):
        """
        Tests that the form is not valid if the data sent is the id of a page in draft.
        """
        page_id = EditorialPage.objects.get(slug='level1-b').pk
        form = ExportForm(data={
            'pages': [page_id]
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                'pages': [
                    'Select a valid choice. {} is not one of the available choices.'.format(page_id)
                ]
            }
        )

    @mock.patch('exporter.forms.actions')
    def test_save(self, mocked_actions):
        """
        Tests that the form is valid and save calls the export action.
        """
        page_id = EditorialPage.objects.get(slug='level1-c').pk
        build_dir = 'temp'
        form = ExportForm(data={
            'pages': [page_id]
        })

        self.assertTrue(form.is_valid())
        form.save(build_dir=build_dir)
        mocked_actions.export.assert_called_with(
            build_dir=build_dir, page_ids=[str(page_id)]
        )
