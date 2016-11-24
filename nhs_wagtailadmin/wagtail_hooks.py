from django.templatetags.static import static
from django.utils.html import format_html
from wagtail.wagtailcore import hooks


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>'.format(
            static('nhs_wagtailadmin/js/revision-preview.js')
        )
    )
