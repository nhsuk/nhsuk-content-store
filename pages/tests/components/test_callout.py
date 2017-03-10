from unittest import TestCase

from ...components.callout import callout, callout_compact


class CalloutTestCase(TestCase):
    def test_children_components_of_callout(self):
        """
        Tests that `callout` has a children stream prop with multiple sub-components
        """
        _, block = callout.as_tuple()

        children_prop = block.child_blocks['children']
        self.assertCountEqual(
            children_prop.child_blocks.keys(),
            ['text', 'reveal']
        )

    def test_children_components_of_callout_compact(self):
        """
        Tests that `callout_compact` has a children stream prop with just `text` as sub-component.
        """
        _, block = callout_compact.as_tuple()

        children_prop = block.child_blocks['children']
        self.assertCountEqual(
            children_prop.child_blocks.keys(),
            ['text']
        )
