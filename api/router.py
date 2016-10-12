from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from wagtail.api.v2.endpoints import PagesAPIEndpoint as WagtailPagesAPIEndpoint
from wagtail.api.v2.router import WagtailAPIRouter

api_router = WagtailAPIRouter('wagtailapi')


class PagesAPIEndpoint(WagtailPagesAPIEndpoint):
    renderer_classes = [CamelCaseJSONRenderer]

api_router.register_endpoint('pages', PagesAPIEndpoint)
