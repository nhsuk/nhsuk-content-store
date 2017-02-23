import copy
from unittest import TestCase, mock

from images.factories import ImageFactory

from .. import components

DEFAULT_MD_COMPONENT_DATA = {
    'type': 'text',
    'props': {
        'variant': 'markdown',
        'value': 'lorem ipsum'
    }
}


class TextComponentTestCase(TestCase):
    def test_doesnt_change_data_if_isnt_markdown(self):
        """
        If component['type']['variant'] isn't 'markdown',
        the data shouldn't change
        """
        data = copy.deepcopy(DEFAULT_MD_COMPONENT_DATA)
        data['props']['variant'] = 'plain'

        component = components.TextComponent(context={})
        transformed_data = component.transform(data)
        self.assertDictEqual(data, transformed_data)

    def test_without_new_files(self):
        """
        If component['type']['variant'] is 'markdown' and context['new_files'] doesn't exist,
        the method should tranform data to value == '!file=content-1.md' and context['new_files'] should
        include a tuple of ('path-to-file-content-1.md', 'content of file')
        """
        data = copy.deepcopy(DEFAULT_MD_COMPONENT_DATA)

        context = {
            'item_base_path': '/item/path'
        }
        component = components.TextComponent(context)
        transformed_data = component.transform(data)

        self.assertNotEqual(data, transformed_data)
        self.assertEqual(transformed_data['props']['value'], '!file=content-1.md')
        self.assertEqual(context['new_files'], [('/item/path/content-1.md', 'lorem ipsum')])

    def test_with_existing_new_files(self):
        """
        If component['type']['variant'] is 'markdown' and context['new_files'] already includes one file,
        the method should tranform data to value == '!file=content-2.md' and context['new_files'] should
        include a tuple of ('path-to-file-content-2.md', 'content of file')
        """
        data = copy.deepcopy(DEFAULT_MD_COMPONENT_DATA)

        context = {
            'item_base_path': '/item/path',
            'new_files': [('/path/file1', 'content')]
        }
        component = components.TextComponent(context)
        transformed_data = component.transform(data)

        self.assertNotEqual(data, transformed_data)
        self.assertEqual(transformed_data['props']['value'], '!file=content-2.md')
        self.assertEqual(
            context['new_files'],
            [('/path/file1', 'content'), ('/item/path/content-2.md', 'lorem ipsum')]
        )


class ImageComponentTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.image = ImageFactory(title='test image')
        self.default_image_data = {
            'type': 'image',
            'props': {
                'id': self.image.id,
                'caption': 'some caption text',
                'alt': 'some alt'
            }
        }

    def transform_from_gallery(self):
        """
        If the image component is part of a gallery, it generates only 2 specs.
        """
        data = self.default_image_data

        context = {
            'page': mock.MagicMock(slug='page'),
            'root_path': '/path/to/root/'
        }
        component = components.ImageComponent(context)
        transformed_data = component.transform(
            data, parent=components.GalleryComponent({})
        )

        slug_postfix = self.image._random_slug_postfix
        self.assertEqual(transformed_data['props']['caption'], data['props']['caption'])
        self.assertEqual(transformed_data['props']['alt'], data['props']['alt'])
        self.assertCountEqual(
            transformed_data['props']['srcset'],
            [
                'assets/images/page/test-image-%s-width-300.png 300w' % slug_postfix,
                'assets/images/page/test-image-%s-width-600.png 600w' % slug_postfix
            ]
        )

    def transform_default(self):
        """
        If the image component is not part of a gallery, it generates 4 different specs.
        """
        data = self.default_image_data

        context = {
            'page': mock.MagicMock(slug='page'),
            'root_path': '/path/to/root/'
        }
        component = components.ImageComponent(context)
        transformed_data = component.transform(data)

        slug_postfix = self.image._random_slug_postfix
        self.assertEqual(transformed_data['props']['caption'], data['props']['caption'])
        self.assertEqual(transformed_data['props']['alt'], data['props']['alt'])
        self.assertCountEqual(
            transformed_data['props']['srcset'],
            [
                'assets/images/page/test-image-%s-width-400.png 400w' % slug_postfix,
                'assets/images/page/test-image-%s-width-640.png 640w' % slug_postfix,
                'assets/images/page/test-image-%s-width-800.png 800w' % slug_postfix,
                'assets/images/page/test-image-%s-width-1280.png 1280w' % slug_postfix
            ]
        )


class StructuralComponentTestCase(object):
    COMPONENT_TYPE = ''
    COMPONENT_CLASS = None
    CHILDREN_PROPS = ['children']

    def test_recursive_transformation(self):
        """
        Tests that if the text component is a child of this structural component, it gets
        transformed recursively.
        """
        data = {
            'type': self.COMPONENT_TYPE,
            'props': {}
        }
        for child_prop in self.CHILDREN_PROPS:
            data['props'][child_prop] = [copy.deepcopy(DEFAULT_MD_COMPONENT_DATA)]

        context = {
            'item_base_path': '/item/path'
        }
        component = self.COMPONENT_CLASS(context)
        transformed_data = component.transform(data)

        for index, child_prop in enumerate(self.CHILDREN_PROPS, start=1):
            self.assertEqual(
                transformed_data['props'][child_prop][0]['props']['value'],
                '!file=content-%s.md' % index
            )


class SplitContentComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'splitContent'
    COMPONENT_CLASS = components.SplitContentComponent


class SplitAreaComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'splitArea'
    COMPONENT_CLASS = components.SplitAreaComponent


class GalleryComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'gallery'
    COMPONENT_CLASS = components.GalleryComponent


class CalloutComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'callout'
    COMPONENT_CLASS = components.CalloutComponent


class PanelComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'panel'
    COMPONENT_CLASS = components.PanelComponent
    CHILDREN_PROPS = ['header', 'body', 'footer']


class RevealComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'reveal'
    COMPONENT_CLASS = components.RevealComponent


class TabsComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'tabs'
    COMPONENT_CLASS = components.TabsComponent


class TabComponentTestCase(StructuralComponentTestCase, TestCase):
    COMPONENT_TYPE = 'tab'
    COMPONENT_CLASS = components.TabComponent
