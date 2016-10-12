from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.contrib import admin
from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls

from api.router import api_router

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(wagtailadmin_urls)),

    url(r'^api/', include(api_router.urls)),

    url(r'', include(wagtail_urls)),
]
