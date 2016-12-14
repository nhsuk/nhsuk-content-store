from django.conf.urls import url
from django.core.urlresolvers import reverse
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import views


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^export-content/$', views.export_content, name='export-content'),
    ]


@hooks.register('register_settings_menu_item')
def register_export_menu_item():
    return MenuItem(
        'Export content',
        reverse('export-content',),
        classnames='icon icon-download',
        order=1100
    )
