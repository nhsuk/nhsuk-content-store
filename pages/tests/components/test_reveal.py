from unittest import TestCase

from ...components.reveal import reveal, reveal_compact


class RevealTestCase(TestCase):
    def test_children_components_of_reveal(self):
        """
        Tests that `reveal` has a children stream prop with multiple sub-components
        """
        _, block = reveal.as_tuple()

        children_prop = block.child_blocks['children']
        self.assertCountEqual(
            children_prop.child_blocks.keys(),
            ['text', 'gallery', 'callout']
        )

    def test_children_components_of_reveal_compact(self):
        """
        Tests that `reveal_compact` has a children stream prop with just `text` as sub-component.
        """
        _, block = reveal_compact.as_tuple()

        children_prop = block.child_blocks['children']
        self.assertCountEqual(
            children_prop.child_blocks.keys(),
            ['text']
        )
