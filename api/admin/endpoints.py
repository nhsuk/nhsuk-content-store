from wagtail.wagtailadmin.api.endpoints import PagesAdminAPIEndpoint as WagtailPagesAdminAPIEndpoint


class PagesAdminAPIEndpoint(WagtailPagesAdminAPIEndpoint):
    @classmethod
    def get_body_fields(cls, model):
        fields = super(PagesAdminAPIEndpoint, cls).get_body_fields(model)

        if hasattr(model, 'admin_api_fields'):
            fields.extend(model.admin_api_fields)

        return fields
