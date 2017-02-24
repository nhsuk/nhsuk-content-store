from unittest import mock

from django.test import TestCase
from rest_framework.fields import CharField

from ..serializers import ContentField


class ContentFieldTestCase(TestCase):
    """
    Tests the ContentField serializer field.
    """
    def setUp(self):
        super().setUp()

        self.serializer_field = ContentField(
            fields=(
                ('field1', CharField),
                ('field2', CharField),
            )
        )

    def test_existing_fields(self):
        """
        Tests that the value returned is a dict of the serialized values of the fields.
        """
        obj = mock.MagicMock(
            field1='value of field 1',
            field2='value of field 2',
        )

        value = self.serializer_field.to_representation(obj)
        self.assertEqual(
            value,
            {
                'field1': 'value of field 1',
                'field2': 'value of field 2'
            }
        )

    def test_non_existing_fields(self):
        """
        Tests that if the obj doesn't have the specific fields, it returns an empty dict.
        """
        class TestObj():
            pass

        value = self.serializer_field.to_representation(TestObj())
        self.assertEqual(
            value, {}
        )

    def test_None(self):
        """
        Tests that if the obj is None, it returns an empty dict.
        """
        value = self.serializer_field.to_representation(None)
        self.assertEqual(
            value, {}
        )
