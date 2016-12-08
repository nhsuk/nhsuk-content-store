from django.core.urlresolvers import reverse
from django.templatetags.static import static
from django.utils.html import format_html_join
from django.utils.six import text_type
from django.utils.translation import ugettext_lazy as _
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks


@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html_join(
        '\n', '<script src="{0}"></script>',
        [
            (static('nhs_wagtailadmin/js/revision-preview.js'),),
        ]
    )


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html_join(
        '\n', '<link rel="stylesheet" href="{0}" type="text/css" />',
        [
            (static('nhs_wagtailadmin/css/nhs-overrides.css'),),
        ]
    )


class DashboardMenuItem(MenuItem):
    def is_active(self, request):
        return request.path == text_type(self.url)


@hooks.register('register_admin_menu_item')
def register_explorer_menu_item():
    return DashboardMenuItem(
        _('Dashboard'), reverse('wagtailadmin_home'),
        name='dashboard',
        classnames='icon icon-wagtail',
        order=50
    )
