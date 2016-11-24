from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from wagtail.wagtailcore import urls as wagtail_urls

from api.router import api_router
from images.views import ServeView
from nhs_wagtailadmin import urls as nhs_wagtailadmin_urls

urlpatterns = [
    url(r'^django-admin/', include(admin.site.urls)),
    url(r'^admin/', include(nhs_wagtailadmin_urls)),

    url(r'^api/', include(api_router.urls)),

    url(
        r'^images/(?P<signature>[^/]*)/(?P<image_id>\d*)/(?P<filter_spec>[^/]*)/\d*/(?P<slug>[^/]*)$',
        ServeView.as_view(), name='images_serve'
    ),
    url(r'', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
