from rest_framework import serializers
from wagtail.api.v2.serializers import PageParentField as WagtailPageParentField
from wagtail.api.v2.serializers import PageSerializer as WagtailPageSerializer
from wagtail.api.v2.serializers import StreamField as WagtailStreamField
from wagtail.api.v2.serializers import Field, get_serializer_class
from wagtail.wagtailcore import fields as wagtailcore_fields

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


class PageSerializer(WagtailPageSerializer):
    serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping.update({
        wagtailcore_fields.StreamField: StreamField
    })
    parent = PageParentField(read_only=True)
    children = PageListField(read_only=True)
    siblings = PageListField(read_only=True)
