from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from oauth2_provider.ext.rest_framework import (
    OAuth2Authentication, TokenHasScope
)
from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter
from wagtail.wagtailimages.api.v2.endpoints import \
    ImagesAPIEndpoint as WagtailImagesAPIEndpoint

from .serializers import PageSerializer

api_router = WagtailAPIRouter('wagtailapi')


class PagesAPIEndpoint(WagtailPagesAPIEndpoint):
    authentication_classes = [OAuth2Authentication]
    permission_classes = [TokenHasScope]
    required_scopes = ['read']

    base_serializer_class = PageSerializer
    renderer_classes = [CamelCaseJSONRenderer]


class ImagesAPIEndpoint(WagtailImagesAPIEndpoint):
    renderer_classes = [CamelCaseJSONRenderer]


api_router.register_endpoint('pages', PagesAPIEndpoint)
api_router.register_endpoint('images', ImagesAPIEndpoint)
