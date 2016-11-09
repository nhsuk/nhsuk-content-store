.. _images:
Images
------

Data
~~~~

Information about images is returned as part of the Content API.

Format::

  {
    "id": 1,
    "meta": {
        "type": "images.Image",
        "detailUrl": "<backend-url>/api/images/1/",
        "tags": []
    },
    "title": "...",
    "width": 1000,
    "height": 500,
    "caption": "",
    "slug": "<slug>.jpeg",
    "version": 1
}

Where:

#. **title**: used for `alt` text
#. **width** and **height**: size of the original image
#. **caption**: caption
#. **slug**: slug of the image. Can be used to compose the image path in a user-friendly way
#. **version**: integer incremented every time the image is saved. Can be used to invalidate the cache when composing the image path


Serving
~~~~~~~

The endpoint for serving images is::

  /images/<signature>/<id>/<filter-spec>/<version>/<slug>

Where:

#. **signature**: is the HMAC of some data using a private key (see below)
#. **id**: id of the image
#. **filter-spec**: spec indicating the size of the image (see below)
#. **version**: integer, version of the image. Only used to invalidate the cache and not actually meaningful
#. **slug**: slug of the image

Example::

  /images/Uo5gv5k9XXsTt6NRHWmGDR4yxC4=/13/width-400/1/chicken-pox.jpg

Signature
#########

``HMAC(K, m)`` where:

#. **K**: shared private key only used for image signatures. See ``settings.IMAGE_SIGNATURE_KEY``
#. **m**: the string ``<image-id>/<filter-spec>/`` e.g. *1/width-800*


Filter Spec
###########

Specifies the size of the image returned.
Possible values (100 and 200 are example values):

#. ``width-100``: width ``100`` and variable height
#. ``height-200``: height ``200`` and variable width
#. ``min-100x200``: variable width and height but trying to keep the values at least 100x200
#. ``max-100x200``: variable width and height but trying to keep the values at most 100x200
#. ``fill-100x200``: crops the image so that the final size is exactly 100x200
#. ``original``: original size
