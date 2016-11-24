Settings
========

Along with the `Django <https://docs.djangoproject.com/en/1.10/ref/settings/>`_
and `Wagtail <http://docs.wagtail.io/en/latest/>`_ settings, there are a few NHS.UK specific ones.


IMAGE_SIGNATURE_KEY
-------------------

Secret key used to generate and verify signatures during image serving.

This is meant to be shared with the frontend client so that it can generate image paths.

For more info, see :ref:`Images <images>`.

PREVIEW_SIGNATURE_KEY
-------------------

Secret key used to generate the signatures for previewing content.

This is meant to be shared with the frontend client so that it can verify them.

For more info, see :ref:`preview-logic`.

FRONTEND_BASE_URL
-----------------

The base url to the frontend app used when redirecting to live pages.

E.g. ``https://example.com``

FRONTEND_PREVIEW_URL
--------------------

Path to the frontend url that will render the preview content.

E.g. ``'https://example.com/preview/{signature}/{page_id}/{revision_id}'``

The *signature*, *page_id* and *revision_id* vars will be replaced by the actual values dynamically.
