import re
from functools import partial

from wagtail.wagtailcore.blocks import CharBlock, RichTextBlock

from images.blocks import ImageChooserBlock

from .blocks import ListBlock, StaticBlock, StreamBlock, StructBlock

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


class Components(object):
    TYPES = {
        'markdown': RichTextBlock,
        'image': ImageChooserBlock,
        'figureList': partial(ListBlock, ImageChooserBlock()),
        'sectionList': section_list,
        'sectionNav': partial(StaticBlock, 'Section Navigation')
    }

    @classmethod
    def get(cls, _type):
        label = LABEL_RE.sub("\g<1> \g<2>", _type).lower()
        return (_type, cls.TYPES[_type](label=label))
