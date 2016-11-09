Content API
-----------

Authentication
~~~~~~~~~~~~~~

To get the content, a client needs to have a OAuth2 Bearer Token.

The oauth flow has not been publicly exposed so you'll have to created one manually if you own the Authentication
Server or ask NHS.UK for one if you want to set up a client.

A default OAuth client and access token for the NHS.UK frontend app is created automatically during the db migration
process. This can be obtained via the django admin area or by quering the db.

When requesting some content, you need to supply the access token as a ``Authorization request header`` e.g.::

  curl -v https://<url>/ -H 'Authorization: Bearer <access-token>'

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

Get live page by id
###################
::

  /api/pages/<id>/

Returns the details of the page with given id split into ``meta`` fields and page fields.

Example of response::

  {
      "id": 5,
      "meta": {
          ...
      },
      "title": "...",
      ...
      <other fields>
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
