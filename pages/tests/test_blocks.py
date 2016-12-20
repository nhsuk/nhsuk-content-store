
from django.test import TestCase
from wagtail.wagtailcore.blocks.field_block import CharBlock
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue

from pages.blocks import ListBlock, StreamBlock, StructBlock


class TestCharBlock(CharBlock):
    def __init__(self, *args, **kwargs):
        self.expected = kwargs.pop('expected', None)
        super(TestCharBlock, self).__init__(*args, **kwargs)

    def to_api_representation(self, value, context=None):
        return self.expected


class StreamBlockTestCase(TestCase):
    def test_api_representation_with_empty_list(self):
        block = StreamBlock([
            ('test', TestCharBlock())
        ])

        representation = block.to_api_representation(
            StreamValue(block, [], is_lazy=True),
            context={}
        )
        self.assertEqual(representation, [])

    def test_api_representation_None_value_gets_skipped(self):
        block = StreamBlock([
            ('test', TestCharBlock(expected=None))
        ])

        representation = block.to_api_representation(
            StreamValue(block, [{'type': 'test', 'value': None}], is_lazy=True),
            context={}
        )
        self.assertEqual(
            representation,
            []
        )

    def test_api_representation_with_value(self):
        expected = 'representation value'

        block = StreamBlock([
            ('test', TestCharBlock(expected=expected))
        ])

        representation = block.to_api_representation(
            StreamValue(block, [{'type': 'test', 'value': 'some value'}], is_lazy=True),
            context={}
        )
        self.assertEqual(
            representation,
            [{'type': 'test', 'value': expected}]
        )


class ListBlockTestCase(TestCase):
    def test_api_representation_with_empty_list(self):
        block = ListBlock(
            TestCharBlock()
        )

        representation = block.to_api_representation([], context={})
        self.assertEqual(representation, [])

    def test_api_representation_None_value_gets_skipped(self):
        block = ListBlock(
            TestCharBlock(expected=None)
        )

        representation = block.to_api_representation([None], context={})
        self.assertEqual(representation, [])

    def test_api_representation_with_value(self):
        expected = 'representation value'

        block = ListBlock(
            TestCharBlock(expected=expected)
        )

        representation = block.to_api_representation(['test'], context={})
        self.assertEqual(representation, [expected])


class StructBlockTestCase(TestCase):
    def test_api_representation_with_empty_list(self):
        block = StructBlock([
            ('test', TestCharBlock())
        ])

        representation = block.to_api_representation(
            StructValue(block, []),
            context={}
        )
        self.assertEqual(representation, {})

    def test_api_representation_with_value(self):
        expected = 'representation value'

        block = StructBlock([
            ('test', TestCharBlock(expected=expected))
        ])

        representation = block.to_api_representation(
            StructValue(block, [('test', 'some value')]),
            context={}
        )
        self.assertEqual(representation, {'test': expected})
