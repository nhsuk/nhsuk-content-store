from unittest import mock

from django.test import TestCase

from pages.factories import (
    ConditionPageFactory, ConditionsPageFactory, SymptomPageFactory,
    SymptomsPageFactory
)

from ..forms import ImportForm


class ImportFormTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # prepare db
        ConditionsPageFactory()
        SymptomsPageFactory()

        # mocked response
        self.mocked_conditions = ['condition-1', 'condition-2', 'condition-3']
        self.mocked_symptoms = ['symptom-1', 'symptom-2', 'symptom-3']

    def get_mocked_list_of_children(self):
        def get_list_of_children(item_type):
            if item_type == 'conditions':
                return self.mocked_conditions
            return self.mocked_symptoms
        return get_list_of_children

    @mock.patch('importer.forms.get_list_of_children_from_remote')
    def test_choices_populated_dynamically(self, mocked_get_list_of_children_from_remote):
        mocked_get_list_of_children_from_remote.side_effect = self.get_mocked_list_of_children()

        form = ImportForm()
        self.assertEqual(
            form.fields['conditions'].choices,
            [(condition, condition) for condition in self.mocked_conditions]
        )
        self.assertEqual(
            form.fields['symptoms'].choices,
            [(symptom, symptom) for symptom in self.mocked_symptoms]
        )

    @mock.patch('importer.forms.get_list_of_children_from_remote')
    def test_existing_pages_unselected(self, mocked_get_list_of_children_from_remote):
        mocked_get_list_of_children_from_remote.side_effect = self.get_mocked_list_of_children()

        ConditionPageFactory(title='condition-2', slug='condition-2')
        ConditionPageFactory(title='different-condition', slug='different-condition')

        SymptomPageFactory(title='symptom-3', slug='symptom-3')

        form = ImportForm()
        self.assertEqual(
            form.fields['conditions'].initial,
            ['condition-1', 'condition-3']
        )

        self.assertEqual(
            form.fields['symptoms'].initial,
            ['symptom-1', 'symptom-2']
        )

    @mock.patch('importer.forms.get_list_of_children_from_remote')
    @mock.patch('importer.forms.Importer')
    def test_save(self, MockedImporter, mocked_get_list_of_children_from_remote):  # NOQA
        mocked_get_list_of_children_from_remote.side_effect = self.get_mocked_list_of_children()

        mocked_importer = MockedImporter()
        form = ImportForm(data={
            'conditions': ['condition-2'],
            'symptoms': ['symptom-3'],
        })
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(mocked_importer.import_items.call_count, 2)

        conditions_call_args = mocked_importer.import_items.call_args_list[0][0]
        self.assertEqual(conditions_call_args[0], 'conditions')
        self.assertEqual(conditions_call_args[1], ['condition-2'])

        symptoms_call_args = mocked_importer.import_items.call_args_list[1][0]
        self.assertEqual(symptoms_call_args[0], 'symptoms')
        self.assertEqual(symptoms_call_args[1], ['symptom-3'])
