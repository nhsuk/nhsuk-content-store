import re
from functools import partial

from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock

from images.blocks import ImageChooserBlock

from .blocks import (
    FixedListBlock, ListBlock, StaticBlock, StreamBlock, StructBlock
)

LABEL_RE = re.compile("([a-z])([A-Z])")


def section_list(**kwargs):
    return StructBlock([
        ('title', CharBlock()),
        ('sections', ListBlock(
            StructBlock([
                ('title', CharBlock()),
                ('content', StreamBlock([
                    Components.get('image'),
                    Components.get('markdown')
                ]))
            ])
        ))
    ], **kwargs)


def panel(**kwargs):
    return StructBlock([
        ('main', RichTextBlock(label='Panel content')),
        ('footer', RichTextBlock(label='Footer content', required=False)),
    ], **kwargs)


def figure_list(**kwargs):
    kwargs['label'] = 'image gallery'
    return ListBlock(
        ImageChooserBlock(), **kwargs
    )


class Components(object):
    TYPES = {
        'markdown': RichTextBlock,
        'panel': panel,
        'splitPanel': partial(FixedListBlock, RichTextBlock()),
        'figureList': figure_list,

        'image': ImageChooserBlock,
        'sectionList': section_list,
        'sectionNav': partial(StaticBlock, admin_text='Section Navigation')
    }

    @classmethod
    def get(cls, _type):
        label = LABEL_RE.sub("\g<1> \g<2>", _type).lower()
        return (_type, cls.TYPES[_type](label=label, icon="radio-full"))
