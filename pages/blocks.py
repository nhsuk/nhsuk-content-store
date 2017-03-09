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
