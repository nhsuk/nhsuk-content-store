from rest_framework import serializers
from wagtail.api.v2.serializers import PageSerializer as WagtailPageSerializer
from wagtail.api.v2.serializers import StreamField as WagtailStreamField
from wagtail.wagtailcore import fields as wagtailcore_fields

from .utils import get_block_representation


class StreamField(WagtailStreamField):
    def to_representation(self, value):
        return get_block_representation(value.stream_block, value, context=self.context)


class PageSerializer(WagtailPageSerializer):
    serializer_field_mapping = serializers.ModelSerializer.serializer_field_mapping.copy()
    serializer_field_mapping.update({
        wagtailcore_fields.StreamField: StreamField,
    })
