Content API
-----------


Endpoints
~~~~~~~~~

Get all live pages
##################
::

  /api/pages/

Returns the list of all live pages in basic format which does not include all the fields.

Example of response::

  {
      "meta": {
          "totalCount": 2
      },
      "items": [
          {
              "id": 1,
              "meta": {
                  ...
              },
              "title": "..."
          },
          ...
      ]
  }

.. _get_page_by_id:

Get a live page by id
#####################
::

  /api/pages/<id>/

  e.g. /api/pages/1/

Returns the details of the page with given id split into ``meta`` fields and page fields.

Example of response::

  {
      "id": 5,
      "meta": {
          ...
      },

      "title": "...",
      ...
  }

Get a live page by path
#######################

::

  /api/pages/with-path/<path>/

  e.g. /api/pages/with-path/conditions/hernia/

Returns the details of the page with given path split into ``meta`` fields and page fields.

The response is exactly the same as the one returned by :ref:`get_page_by_id`.

Example of response::

  {
      "id": 5,
      "meta": {
          ...
      },

      "title": "...",
      ...
  }


Meta fields
~~~~~~~~~~~

The ``meta`` field defines the following metadata:

#. **type**: the page type. E.g. ``pages.EditorialPage``
#. **slug**: the relative slug value of the page. Note that this does not include the parent path
#. **parent**: details of the parent page in basic mode
#. **children**: ordered list of live child pages in basic mode
#. **siblings**: ordered list of live siblings, including the current page, in basic mode
