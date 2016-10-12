from django.core.exceptions import ValidationError
from django.test import TestCase

from wagtailmarkdown.fields import Markdown, MarkdownBlock


class TestMarkdownBlock(TestCase):
    def test_get_default_with_fallback_value(self):
        default_value = MarkdownBlock().get_default()
        self.assertIsInstance(default_value, Markdown)
        self.assertEqual(default_value.source, '')

    def test_get_default_with_default_none(self):
        default_value = MarkdownBlock(default=None).get_default()
        self.assertIsInstance(default_value, Markdown)
        self.assertEqual(default_value.source, '')

    def test_get_default_with_empty_string(self):
        default_value = MarkdownBlock(default='').get_default()
        self.assertIsInstance(default_value, Markdown)
        self.assertEqual(default_value.source, '')

    def test_get_default_with_nonempty_string(self):
        default_value = MarkdownBlock(default='# title').get_default()
        self.assertIsInstance(default_value, Markdown)
        self.assertEqual(default_value.source, '# title')

    def test_get_default_with_markdown_value(self):
        default_value = MarkdownBlock(default=Markdown('# title')).get_default()
        self.assertIsInstance(default_value, Markdown)
        self.assertEqual(default_value.source, '# title')

    def test_validate_required_markdown_block(self):
        block = MarkdownBlock()

        with self.assertRaises(ValidationError):
            block.clean(Markdown(''))

    def test_validate_non_required_markdown_block(self):
        block = MarkdownBlock(required=False)
        result = block.clean(Markdown(''))
        self.assertIsInstance(result, Markdown)
        self.assertEqual(result.source, '')
