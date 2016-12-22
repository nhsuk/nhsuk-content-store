import string

from django.template.loader import render_to_string
from wagtail.wagtailcore.blocks.list_block import ListBlock as WagtailListBlock
from wagtail.wagtailcore.blocks.static_block import \
    StaticBlock as WagtailStaticBlock
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
    def to_api_representation(self, value, context=None):
        if value is None:
            # treat None as identical to an empty stream
            return []

        context = context or {}
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
    def to_api_representation(self, value, context=None):
        # recursively call get_prep_value on children and return as a list
        context = context or {}
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
    def to_api_representation(self, value, context=None):
        # recursively call get_prep_value on children and return as a plain dict
        context = context or {}
        return dict([
            (name, get_block_representation(self.child_blocks[name], val, context))
            for name, val in value.items()
        ])


class StaticBlock(WagtailStaticBlock):
    def value_from_datadict(self, data, files, prefix):
        return self.name


class FixedListBlock(ListBlock):
    """
    Same as ListBlock except:
        - it has a fixed number of members (configurable)
        - members cannot be added/removed/ordered
        - members have a label == `<label> A|B|C|D...` (configurable)
    """
    def __init__(self, *args, **kwargs):
        super(FixedListBlock, self).__init__(*args, **kwargs)

        # checks that number of defaults is not bigger than members number
        if len(self.meta.default) > self.meta.members_number:
            raise TypeError(
                'default length is bigger than members number'
            )

        # add extra defaults if needed
        self.meta.default += [self.child_block.get_default()] * (self.meta.members_number - len(self.meta.default))

    def render_form(self, value, prefix='', errors=None):
        if errors:
            if len(errors) > 1:
                # We rely on FixedListBlock.clean throwing a single ValidationError with a specially crafted
                # 'params' attribute that we can pull apart and distribute to the child blocks
                raise TypeError('FixedListBlock.render_form unexpectedly received multiple errors')
            error_list = errors.as_data()[0].params
        else:
            error_list = None

        list_members_html = [
            self.render_list_member(child_val, "%s-%d" % (prefix, i), i,
                                    errors=error_list[i] if error_list else None)
            for (i, child_val) in enumerate(value)
        ]

        return render_to_string('wagtailadmin/block_forms/fixed_list.html', {
            'help_text': getattr(self.meta, 'help_text', None),
            'prefix': prefix,
            'list_members_html': list_members_html,
        })

    def render_list_member(self, value, prefix, index, errors=None):
        """
        Render the HTML for a single list item in the form. This consists of an <li> wrapper, hidden fields
        to manage ID/deleted state, delete/reorder buttons, and the child block's own form HTML.
        """
        child = self.child_block.bind(value, prefix="%s-value" % prefix, errors=errors)

        return render_to_string('wagtailadmin/block_forms/fixed_list_member.html', {
            'prefix': prefix,
            'child': child,
            'index': index,
            'label': '{} {}'.format(
                self.meta.members_label,
                string.ascii_uppercase[index or 0]
            )
        })

    class Meta:
        members_number = 2
        members_label = 'Area'
