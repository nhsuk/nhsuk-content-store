from wagtail.wagtailcore import hooks

from .admin.endpoints import PagesAdminAPIEndpoint


@hooks.register('construct_admin_api')
def pages_endpoint(router):
    router.register_endpoint('pages', PagesAdminAPIEndpoint)
