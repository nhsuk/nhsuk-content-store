from unittest import TestCase

from wagtail.wagtailcore.rich_text import RichText

from ..page_elements import Components


class PanelComponentTestCase(TestCase):
    def test_component(self):
        _, panel = Components.get('panel')

        api_representation = panel.to_api_representation({
            'main': RichText('# main'),
            'footer': RichText('footer text'),
        })

        self.assertEqual(
            api_representation, {
                'main': '# main',
                'footer': 'footer text'
            }
        )


class MarkdownComponentTestCase(TestCase):
    def test_component(self):
        _, md = Components.get('markdown')

        api_representation = md.get_prep_value(RichText('# text'))
        self.assertEqual(api_representation, '# text')
