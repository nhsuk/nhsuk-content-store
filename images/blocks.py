from wagtail.wagtailimages.blocks import \
    ImageChooserBlock as WagtailImageChooserBlock


class ImageChooserBlock(WagtailImageChooserBlock):
    """
    Same as the Wagtail ImageChooserBlock but denormalising
    the image data in the json response so that we don't have to make an extra call.
    """
    def to_api_representation(self, value, context=None):
        if value is None:
            return None

        context = context or {}
        router = context['router']
        endpoint = router.get_model_endpoint(value.__class__)[1]()
        serializer_class = endpoint._get_serializer_class(router, value.__class__, [], show_details=True)
        return serializer_class(value, context=context).data
