from wagtail.api.v2.serializers import PageParentField as WagtailPageParentField
from wagtail.api.v2.serializers import PageSerializer as WagtailPageSerializer
from wagtail.api.v2.serializers import StreamField as WagtailStreamField
from wagtail.api.v2.serializers import Field, get_serializer_class

from .utils import get_block_representation


class StreamField(WagtailStreamField):
    def to_representation(self, value):
        return get_block_representation(value.stream_block, value, context=self.context)


def get_page_serializer_class(value):
    return get_serializer_class(
        value.__class__,
        ['id', 'type', 'detail_url', 'html_url', 'title', 'slug'],
        meta_fields=['type', 'detail_url', 'html_url'],
        base=PageSerializer
    )


class PageListField(Field):
    """
    Serializes a list of Page objects.
    """
    def to_representation(self, value):
        if not value:
            return []

        serializer_class = get_page_serializer_class(value[0])
        serializer = serializer_class(context=self.context)

        return [
            serializer.to_representation(child_object)
            for child_object in value
        ]


class PageParentField(WagtailPageParentField):
    """
    Like the Wagtail PageParentField but using a consistent page serializer.
    """
    def to_representation(self, value):
        serializer_class = get_page_serializer_class(value)
        serializer = serializer_class(context=self.context)
        return serializer.to_representation(value)


class ContentField(Field):
    """
    Returns a dict of content fields so that they are namespaced and not among other model fields.
    The param `fields` is a list of tuples (field name, serializer field) of the content fields
    to be returned.

    Example of returned value:
        {
            "header": [
              {
                "value": "test header content",
                "type": "markdown"
              }
            ],
            "main": [
              {
                "value": "test main content",
                "type": "markdown"
              }
            ]
        }
    """
    def __init__(self, *args, **kwargs):
        self.fields = kwargs.pop('fields')
        super(ContentField, self).__init__(*args, **kwargs)

    def get_attribute(self, instance):
        return instance

    def to_representation(self, page):
        content = {}

        if page:
            for field_name, serializer_field in self.fields:
                if hasattr(page, field_name):
                    value = getattr(page, field_name)

                    field = serializer_field()
                    field.context = dict(self.context)
                    content[field_name] = field.to_representation(value)
        return content


class PageSerializer(WagtailPageSerializer):
    parent = PageParentField(read_only=True)
    children = PageListField(read_only=True)
    siblings = PageListField(read_only=True)
    content = ContentField(
        fields=[
            ('header', StreamField),
            ('main', StreamField),
        ],
        read_only=True
    )
