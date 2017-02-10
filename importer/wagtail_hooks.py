from django.conf.urls import url
from django.core.urlresolvers import reverse
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from . import views


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^import-content/$', views.import_content, name='import-content'),
    ]


@hooks.register('register_settings_menu_item')
def register_import_menu_item():
    return MenuItem(
        'Import content',
        reverse('import-content',),
        classnames='icon icon-collapse-up',
        order=1200
    )
