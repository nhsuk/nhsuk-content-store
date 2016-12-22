from unittest import TestCase

from django.forms.utils import ErrorList
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks.field_block import CharBlock
from wagtail.wagtailcore.blocks.stream_block import StreamValue
from wagtail.wagtailcore.blocks.struct_block import StructValue

from pages.blocks import FixedListBlock, ListBlock, StreamBlock, StructBlock


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


class FixedListBlockTestCase(TestCase):
    def test_initialise_with_class(self):
        block = FixedListBlock(blocks.CharBlock)

        # Child block should be initialised for us
        self.assertIsInstance(block.child_block, blocks.CharBlock)

    def test_initialise_with_instance(self):
        child_block = blocks.CharBlock()
        block = FixedListBlock(child_block)

        self.assertEqual(block.child_block, child_block)

    def render_form(self):
        class LinkBlock(blocks.StructBlock):
            title = blocks.CharBlock()
            link = blocks.URLBlock()

        block = FixedListBlock(LinkBlock)

        html = block.render_form([
            {
                'title': "Wagtail",
                'link': 'http://www.wagtail.io',
            },
            {
                'title': "Django",
                'link': 'http://www.djangoproject.com',
            },
        ], prefix='links')

        return html

    def test_render_form_wrapper_class(self):
        html = self.render_form()

        self.assertIn('<div class="sequence-container sequence-type-fixed-list">', html)

    def test_hidden_list_inputs(self):
        html = self.render_form()

        self.assertIn('<input type="hidden" name="links-count" id="links-count" value="2">', html)
        self.assertIn('<input type="hidden" id="links-0-deleted" name="links-0-deleted" value="">', html)
        self.assertIn('<input type="hidden" id="links-0-order" name="links-0-order" value="0">', html)
        self.assertIn('<input type="hidden" id="links-1-order" name="links-1-order" value="1">', html)

    def test_render_form_values(self):
        html = self.render_form()

        self.assertIn(
            (
                '<input id="links-0-value-title" name="links-0-value-title" placeholder="Title"'
                ' type="text" value="Wagtail" />'
            ),
            html
        )
        self.assertIn(
            (
                '<input id="links-0-value-link" name="links-0-value-link" placeholder="Link" type="url"'
                ' value="http://www.wagtail.io" />'
            ),
            html
        )
        self.assertIn(
            (
                '<input id="links-1-value-title" name="links-1-value-title" placeholder="Title" type="text"'
                ' value="Django" />'
            ),
            html
        )
        self.assertIn(
            (
                '<input id="links-1-value-link" name="links-1-value-link" placeholder="Link"'
                ' type="url" value="http://www.djangoproject.com" />'
            ),
            html
        )

    def test_render_form_errors_with_multiple_errors(self):
        class LinkBlock(blocks.StructBlock):
            title = blocks.CharBlock()
            link = blocks.URLBlock()

        block = FixedListBlock(LinkBlock)

        self.assertRaises(
            TypeError,
            block.render_form,
            [
                {
                    'title': "Wagtail",
                    'link': 'http://www.wagtail.io',
                },
                {
                    'title': "Django",
                    'link': 'http://www.djangoproject.com',
                },
            ],
            prefix='links',
            errors=ErrorList(['error1', 'error2'])
        )

    def test_html_declarations(self):
        class LinkBlock(blocks.StructBlock):
            title = blocks.CharBlock()
            link = blocks.URLBlock()

        block = FixedListBlock(LinkBlock)
        html = block.html_declarations()

        self.assertIn(
            '<input id="__PREFIX__-value-title" name="__PREFIX__-value-title" placeholder="Title" type="text" />',
            html
        )
        self.assertIn(
            '<input id="__PREFIX__-value-link" name="__PREFIX__-value-link" placeholder="Link" type="url" />',
            html
        )

    def test_can_specify_default(self):
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock(), default=['peas', 'beans'])

        block = ShoppingListBlock()
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn(
            '<input type="hidden" name="shoppinglist-items-count" id="shoppinglist-items-count" value="2">',
            form_html
        )
        self.assertIn('value="peas"', form_html)
        self.assertIn('value="beans"', form_html)

    def test_default_default(self):
        """
        if no explicit 'default' is set on the FixedListBlock, it should fall back on
        2 instances of the child block in its default state.
        """
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock(default='chocolate'))

        block = ShoppingListBlock()
        # the value here does not specify an 'items' field, so this should revert to the ListBlock's default
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn(
            '<input type="hidden" name="shoppinglist-items-count" id="shoppinglist-items-count" value="2">',
            form_html
        )
        self.assertIn('value="chocolate"', form_html)

    def test_can_specify_members_number(self):
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock(), members_number=3)

        block = ShoppingListBlock()
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn(
            '<input type="hidden" name="shoppinglist-items-count" id="shoppinglist-items-count" value="3">',
            form_html
        )

    def test_default_members_number(self):
        """
        `members_number` should default to 2 if not overridden.
        """
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock())

        block = ShoppingListBlock()
        # the value here does not specify an 'items' field, so this should revert to the ListBlock's default
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn(
            '<input type="hidden" name="shoppinglist-items-count" id="shoppinglist-items-count" value="2">',
            form_html
        )

    def test_fails_if_length_of_default_is_greater_than_members_number(self):
        self.assertRaises(
            TypeError,
            FixedListBlock,
            blocks.CharBlock(),
            members_number=2,
            default=['peas', 'beans', 'carrots']
        )

    def test_can_specify_members_label(self):
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock(), members_label='Section')

        block = ShoppingListBlock()
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn('<label>Section A:</label>', form_html)
        self.assertIn('<label>Section B:</label>', form_html)

    def test_default_members_label(self):
        class ShoppingListBlock(blocks.StructBlock):
            shop = blocks.CharBlock()
            items = FixedListBlock(blocks.CharBlock())

        block = ShoppingListBlock()
        form_html = block.render_form(block.to_python({'shop': 'Tesco'}), prefix='shoppinglist')

        self.assertIn('<label>Area A:</label>', form_html)
        self.assertIn('<label>Area B:</label>', form_html)
