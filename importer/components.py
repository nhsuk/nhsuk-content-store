import os
import re
import sys

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from images.models import Image

from .utils import get_data_from_remote


class Component(object):
    def __init__(self, context):
        self.context = context

    def transform(self, data):
        raise NotImplementedError()


class StructuralComponent(Component):
    COMPONENTS = {
        'text': 'TextComponent',
        'split_content': 'SplitContentComponent',
        'split_area': 'SplitAreaComponent',
        'gallery': 'GalleryComponent',
        'image': 'ImageComponent',
        'callout': 'CalloutComponent',
        'panel': 'PanelComponent',
        'reveal': 'RevealComponent',
        'tabs': 'TabsComponent',
        'tab': 'TabComponent',
    }

    def load_component(self, component_type):
        component = getattr(
            sys.modules[__name__],
            self.COMPONENTS[component_type]
        )
        return component(self.context)

    def transform_components(self, data):
        transformed_data = []
        for comp_data in data:
            component = self.load_component(comp_data['type'])
            transformed_data.append(
                component.transform(comp_data)
            )
        return transformed_data


class TextComponent(Component):
    @property
    def item_base_url(self):
        return self.context['item_base_url']

    def get_value_from_file(self, include_file):
        return get_data_from_remote('%s/%s' % (self.item_base_url, include_file))

    def get_value(self, val):
        if val.startswith('!file='):
            return self.get_value_from_file(val.split('!file=')[1])
        return val

    def transform(self, data):
        return {
            'type': data['type'],
            'value': {
                'variant': data['props']['variant'],
                'value': self.get_value(data['props']['value'])
            }
        }


class ImageComponent(Component):
    def find_biggest_image(self, srcset):
        found = (None, -1)
        for src in srcset:
            path, size = src.split(' ')
            size = int(re.search(r'\d+', size).group())
            if size > found[1]:
                found = (path, size)
        return path

    @property
    def assets_base_url(self):
        return self.context['assets_base_url']

    def get_image_data_from_file(self, include_file):
        return get_data_from_remote('%s/%s' % (self.assets_base_url, include_file), is_file=True)

    def transform(self, data):
        path = self.find_biggest_image(data['props']['srcset'])
        name = os.path.basename(path)

        image = Image(
            caption=data['props'].get('caption', ''),
            title=data['props']['alt']
        )

        # save temp file
        img_temp = NamedTemporaryFile()
        img_temp.write(self.get_image_data_from_file(path))
        img_temp.flush()

        # save file and image
        image.file.save(name, File(img_temp), save=True)
        image.save()

        return {
            'type': 'image',
            'value': image.id
        }


class SplitContentComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'splitContent',
            'value': {
                'children': self.transform_components(data['props']['children'])
            }
        }


class SplitAreaComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'splitArea',
            'value': {
                'children': self.transform_components(data['props']['children'])
            }
        }


class GalleryComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'gallery',
            'value': {
                'children': self.transform_components(data['props']['children'])
            }
        }


class CalloutComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'callout',
            'value': {
                'variant': data['props']['variant'],
                'compact': data['props'].get('compact', False),
                'children': self.transform_components(data['props']['children'])
            }
        }


class PanelComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'panel',
            'value': {
                'header': self.transform_components(data['props'].get('header', [])),
                'body': self.transform_components(data['props'].get('body', [])),
                'footer': self.transform_components(data['props'].get('footer', []))
            }
        }


class RevealComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'reveal',
            'value': {
                'summary': data['props']['summary'],
                'variant': data['props']['variant'],
                'children': self.transform_components(data['props']['children'])
            }
        }


class TabsComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'tabs',
            'value': {
                'variant': data['props']['variant'],
                'children': self.transform_components(data['props']['children'])
            }
        }


class TabComponent(StructuralComponent):
    def transform(self, data):
        return {
            'type': 'tab',
            'value': {
                'label': data['props']['label'],
                'children': self.transform_components(data['props']['children'])
            }
        }
