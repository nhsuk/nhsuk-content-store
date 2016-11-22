Content Preview API
-------------------


Endpoints
~~~~~~~~~

Get a version of the page
#########################
::

  /api/preview-pages/<page-id>/?revision-id=<revision-id>

  e.g. /api/preview-pages/5/?revision-id=8

Returns the content of the page with id == ``page-id`` for the revision
with id == ``revision-id`` if specified, or the latest revision otherwise.

The response is exactly the same as the one returned by :ref:`get_page_by_id`.
