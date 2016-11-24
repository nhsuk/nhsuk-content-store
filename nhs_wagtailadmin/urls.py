from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.views.decorators.cache import cache_control
from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailadmin.decorators import require_admin_access

from . import views

# override wagtail views
urlpatterns = [
    url(r'^pages/add/(\w+)/(\w+)/(\d+)/preview/$', views.preview_via_POST_deprecated, name='preview_on_add'),
    url(r'^pages/(\d+)/edit/preview/$', views.preview_via_POST_deprecated, name='preview_on_edit'),

    url(r'^pages/preview/$', views.preview_via_POST_deprecated, name='preview'),
    url(r'^pages/preview_loading/$', views.preview_via_POST_deprecated, name='preview_loading'),

    url(r'^pages/(\d+)/view_draft/$', views.view_draft, name='view_draft'),

    url(r'^pages/moderation/(\d+)/preview/$', views.preview_for_moderation, name='preview_for_moderation'),

    url(r'^pages/(\d+)/revisions/(\d+)/view/$', views.revisions_view, name='revisions_view'),
]

# Add "wagtailadmin.access_admin" permission check
urlpatterns = decorate_urlpatterns(urlpatterns, require_admin_access)

# Decorate all views with cache settings to prevent caching
urlpatterns = decorate_urlpatterns(
    urlpatterns,
    cache_control(private=True, no_cache=True, no_store=True, max_age=0)
)

# include the rest of the wagtail views
urlpatterns += [
    url(r'^', include(wagtailadmin_urls)),
]
