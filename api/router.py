from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import \
    ImagesAPIEndpoint as WagtailImagesAPIEndpoint

from .serializers import PageSerializer

api_router = WagtailAPIRouter('wagtailapi')


class PagesAPIEndpoint(WagtailPagesAPIEndpoint):
    base_serializer_class = PageSerializer
    renderer_classes = [CamelCaseJSONRenderer]


class ImagesAPIEndpoint(WagtailImagesAPIEndpoint):
    renderer_classes = [CamelCaseJSONRenderer]


api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
