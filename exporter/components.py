import copy
import os
import sys


class Component(object):
    def __init__(self, context):
        self.context = context

    def transform(self, data):
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

    def transform_components(self, data):
        transformed_data = []
        for comp_data in data:
            component = self.load_component(comp_data['type'])
            transformed_data.append(
                component.transform(comp_data)
            )
        return transformed_data

    def transform(self, data):
        transformed_data = copy.deepcopy(data)
        for child_prop in self.CHILDREN_PROPS:
            transformed_data['props'][child_prop] = self.transform_components(
                transformed_data['props'][child_prop]
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

    def transform(self, data):
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
    def transform(self, data):
        return data


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
