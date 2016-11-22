Authentication
--------------

To get the content (live or preview), a client needs to have a OAuth2 Bearer Token.

The oauth flow has not been publicly exposed so you'll have to created one manually if you own the Authentication
Server or ask NHS.UK for one if you want to set up a client.

A default OAuth client and access token for the NHS.UK frontend app is created automatically during the db migration
process. This can be obtained via the django admin area or by quering the db.

When requesting some content, you need to supply the access token as a ``Authorization request header`` e.g.::

  curl -v https://<url>/ -H 'Authorization: Bearer <access-token>'
