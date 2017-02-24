import imghdr
from wsgiref.util import FileWrapper

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.http import (
    HttpResponse, HttpResponsePermanentRedirect, StreamingHttpResponse
)
from django.shortcuts import get_object_or_404
from django.utils.decorators import classonlymethod
from django.views.generic import View
from wagtail.wagtailimages import get_image_model
from wagtail.wagtailimages.exceptions import InvalidFilterSpecError
from wagtail.wagtailimages.models import SourceImageIOError
from wagtail.wagtailimages.views.serve import verify_signature


class ServeView(View):
    model = get_image_model()
    action = 'serve'
    key = settings.IMAGE_SIGNATURE_KEY

    @classonlymethod
    def as_view(cls, **initkwargs):  # noqa
        if 'action' in initkwargs:
            if initkwargs['action'] not in ['serve', 'redirect']:
                raise ImproperlyConfigured("ServeView action must be either 'serve' or 'redirect'")

        return super().as_view(**initkwargs)

    def get(self, request, signature, image_id, filter_spec, slug):
        if not verify_signature(signature.encode(), image_id, filter_spec, key=self.key):
            raise PermissionDenied

        image = get_object_or_404(self.model, id=image_id, slug=slug)

        # Get/generate the rendition
        try:
            rendition = image.get_rendition(filter_spec)
        except SourceImageIOError:
            return HttpResponse("Source image file not found", content_type='text/plain', status=410)
        except InvalidFilterSpecError:
            return HttpResponse("Invalid filter spec: " + filter_spec, content_type='text/plain', status=400)

        return getattr(self, self.action)(rendition)

    def serve(self, rendition):
        # Open and serve the file
        rendition.file.open('rb')
        image_format = imghdr.what(rendition.file)
        return StreamingHttpResponse(FileWrapper(rendition.file),
                                     content_type='image/' + image_format)

    def redirect(self, rendition):
        # Redirect to the file's public location
        return HttpResponsePermanentRedirect(rendition.url)
