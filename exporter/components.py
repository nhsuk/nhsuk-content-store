import copy
import os
import sys

from images.models import Image


class Component(object):
    def __init__(self, context):
        self.context = context

    def transform(self, data, **kwargs):
        return data


class StructuralComponent(Component):
    COMPONENTS = {
        'text': 'TextComponent',
        'splitContent': 'SplitContentComponent',
        'splitArea': 'SplitAreaComponent',
        'gallery': 'GalleryComponent',
        'image': 'ImageComponent',
        'callout': 'CalloutComponent',
        'panel': 'PanelComponent',
        'reveal': 'RevealComponent',
        'tabs': 'TabsComponent',
        'tab': 'TabComponent',
    }
    CHILDREN_PROPS = ['children']

    def load_component(self, component_type):
        component = getattr(
            sys.modules[__name__],
            self.COMPONENTS[component_type]
        )
        return component(self.context)

    def transform_components(self, data, **kwargs):
        transformed_data = []
        for comp_data in data:
            component = self.load_component(comp_data['type'])
            transformed_data.append(
                component.transform(comp_data, **kwargs)
            )
        return transformed_data

    def transform(self, data, **kwargs):
        transformed_data = copy.deepcopy(data)
        kwargs['parent'] = self
        for child_prop in self.CHILDREN_PROPS:
            transformed_data['props'][child_prop] = self.transform_components(
                transformed_data['props'][child_prop],
                **kwargs
            )
        return transformed_data


class TextComponent(Component):
    MD_FILENAME_FORMAT = 'content-{count}.md'

    @property
    def md_files(self):
        if 'new_files' not in self.context:
            self.context['new_files'] = []
        return self.context['new_files']

    @property
    def item_base_path(self):
        return self.context['item_base_path']

    def get_build_path(self, filename):
        return os.path.join(self.item_base_path, filename)

    def transform(self, data, **kwargs):
        """
        Converts md content into '!file=content-n.md' value and populates the
        'new_files' list with the extra file to create.
        This is so that md content is saved into external and more manageable files.
        """
        if data['props']['variant'] != 'markdown':
            return data

        md_content = data['props']['value']
        md_filename = self.MD_FILENAME_FORMAT.format(count=(len(self.md_files) + 1))

        return_data = copy.deepcopy(data)
        return_data['props']['value'] = '!file=%s' % md_filename

        self.md_files.append(
            (self.get_build_path(md_filename), md_content)
        )

        return return_data


class ImageComponent(Component):
    DEFAULT_SIZES = ['300', '600']
    IN_GALLERY_SIZES = ['400', '640', '800', '1280']
    IMAGES_ROOT = 'assets/images'

    def get_sizes(self, parent):
        if not parent or not isinstance(parent, GalleryComponent):
            return self.IN_GALLERY_SIZES
        return self.DEFAULT_SIZES

    @property
    def image_files(self):
        if 'new_files' not in self.context:
            self.context['new_files'] = []
        return self.context['new_files']

    @property
    def root_path(self):
        return self.context['root_path']

    @property
    def page(self):
        return self.context['page']

    @property
    def images_path(self):
        return os.path.join(self.root_path, 'images')

    def get_build_path(self, size, obj):
        """
        Returns a tuple of (relative path, absolute path) related to the object `obj`
        with size `size`.
        """
        filename, file_extension = os.path.splitext(obj.slug)
        built_name = '{}-{}{}'.format(filename, size, file_extension)
        relative_path = os.path.join(self.page.slug, built_name)
        absolute_path = os.path.join(self.images_path, relative_path)

        return (relative_path, absolute_path)

    def transform(self, data, **kwargs):
        """
        Converts image components into srcsets with related image specs
        whilst populating the 'new_files' list with the image files to create.
        """
        image = Image.objects.get(pk=data['props']['id'])
        sizes = self.get_sizes(kwargs.get('parent'))

        srcset = []
        for size in sizes:
            spec = 'width-%s' % size
            rendition = image.get_rendition(spec)
            relative_path, absolute_path = self.get_build_path(spec, image)
            srcset.append(
                '{}/{} {}w'.format(self.IMAGES_ROOT, relative_path, size)
            )

            self.image_files.append(
                (absolute_path, rendition)
            )

        return {
            'type': 'image',
            'props': {
                'alt': data['props']['alt'],
                'caption': data['props']['caption'],
                'srcset': srcset
            }
        }


class SplitContentComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class SplitAreaComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class GalleryComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class CalloutComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class PanelComponent(StructuralComponent):
    CHILDREN_PROPS = ['header', 'body', 'footer']


class RevealComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class TabsComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']


class TabComponent(StructuralComponent):
    CHILDREN_PROPS = ['children']
