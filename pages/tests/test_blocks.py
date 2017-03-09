from unittest import TestCase

from wagtail.wagtailcore.blocks.field_block import CharBlock
from wagtail.wagtailcore.blocks.stream_block import StreamValue

from pages.blocks import StreamBlock


class TestCharBlock(CharBlock):
    def __init__(self, *args, **kwargs):
        self.expected = kwargs.pop('expected', None)
        super().__init__(*args, **kwargs)

    def get_api_representation(self, value, context=None):
        return self.expected


class StreamBlockTestCase(TestCase):
    def test_api_representation_with_empty_list(self):
        block = StreamBlock([
            ('test', TestCharBlock())
        ])

        representation = block.get_api_representation(
            StreamValue(block, [], is_lazy=True),
            context={}
        )
        self.assertEqual(representation, [])

    def test_api_representation_with_value(self):
        expected = 'representation value'

        block = StreamBlock([
            ('test', TestCharBlock(expected=expected))
        ])

        representation = block.get_api_representation(
            StreamValue(block, [{'type': 'test', 'value': 'some value'}], is_lazy=True),
            context={}
        )
        self.assertEqual(
            representation,
            [{'type': 'test', 'props': expected}]
        )
