from wagtail.wagtailcore.blocks import Block
from wagtail.wagtailcore.blocks.list_block import ListBlock as WagtailListBlock
from wagtail.wagtailcore.blocks.stream_block import \
    StreamBlock as WagtailStreamBlock
from wagtail.wagtailcore.blocks.struct_block import \
    StructBlock as WagtailStructBlock

from api.utils import get_block_representation


class StreamBlock(WagtailStreamBlock):
    """
    Same as the Wagtail StreamBlock but with the ability to choose a different
    representation during a json API response.
    """
    def to_api_representation(self, value, context={}):
        if value is None:
            # treat None as identical to an empty stream
            return []

        output = []
        for child in value:
            represented_value = get_block_representation(child.block, child.value, context)
            if represented_value:
                # if the value is a related obj and it gets deleted, represented_value == None so we skip it
                output.append({
                    'type': child.block.name,
                    'value': represented_value
                })
        return output


class ListBlock(WagtailListBlock):
    """
    Same as the Wagtail ListBlock but with the ability to choose a different
    representation during a json API response.
    """
    def to_api_representation(self, value, context={}):
        # recursively call get_prep_value on children and return as a list
        output = []
        for item in value:
            represented_value = get_block_representation(self.child_block, item, context)
            if represented_value:
                # if the value is a related obj and it gets deleted, represented_value == None so we skip it
                output.append(represented_value)
        return output


class StructBlock(WagtailStructBlock):
    """
    Same as the Wagtail StructBlock but with the ability to choose a different
    representation during a json API response.
    """
    def to_api_representation(self, value, context={}):
        # recursively call get_prep_value on children and return as a plain dict
        return dict([
            (name, get_block_representation(self.child_blocks[name], val, context))
            for name, val in value.items()
        ])


class StaticBlock(Block):
    """
    Very simple static block that only returns the value given as init param.
    When added to a page, the frontend can use it to trigger some related logic that doesn't
    require any particular dynamic block content.
    """
    def __init__(self, value, *args, **kwargs):
        self.value = value
        super(StaticBlock, self).__init__(*args, **kwargs)

    def render_form(self, *args, **kwargs):
        return self.value

    def value_from_datadict(self, *args, **kwargs):
        return self.value

    class Meta:
        default = None
