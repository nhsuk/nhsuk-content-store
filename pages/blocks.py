import string

from django.template.loader import render_to_string
from wagtail.wagtailcore.blocks.list_block import ListBlock
from wagtail.wagtailcore.blocks.stream_block import \
    StreamBlock as WagtailStreamBlock


class StreamBlock(WagtailStreamBlock):
    """
    Same as the Wagtail StreamBlock with a 'props' key instead of 'value'.
    """
    def get_api_representation(self, value, context=None):
        output = super().get_api_representation(value, context=context)
        if output:
            output = [{'type': item['type'], 'props': item['value']} for item in output]
        return output


class FixedListBlock(ListBlock):
    """
    Same as ListBlock except:
        - it has a fixed number of members (configurable)
        - members cannot be added/removed/ordered
        - members have a label == `<label> A|B|C|D...` (configurable)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
