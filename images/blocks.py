from wagtail.wagtailimages.blocks import \
    ImageChooserBlock as WagtailImageChooserBlock


class ImageChooserBlock(WagtailImageChooserBlock):
    """
    Same as the Wagtail ImageChooserBlock but denormalising
    the image data in the json response so that we don't have to make an extra call.
    """
    def get_api_representation(self, value, context=None):
        from wagtail.wagtailimages.api.v2.endpoints import ImagesAPIEndpoint

        if value is None or not context:
            return None

        endpoint = ImagesAPIEndpoint()
        serializer_class = endpoint._get_serializer_class(
            context['router'], value.__class__, [], show_details=True
        )
        return serializer_class(value, context=context).data
