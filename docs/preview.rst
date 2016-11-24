.. _preview-logic:

Preview logic
=============

Background
----------

As you know, the architecture is split into a `Publishing Tool app`_ defining the
API and a `Frontend app`_ using the API to render the content.

The Publishing Tool has an admin area where content designers can create content and preview it.

As the Frontend app is responsible for rendering the content, the Publishing Tool needs
a way to communicate with the Frontend app when previewing content.

The Frontend app can get the preview content passing the ``page-id`` and the ``revision-id`` to the
:ref:`content-preview-api`.


Preview Button
--------------

The Publishing Tool area includes a *Preview Button* that content designers use to preview
the content they are creating.

After pressing the button, the following logic applies:

-  The Publishing Tool saves the page version as a Revision, noting the ``revision-id``
-  The Publishing Tool makes a GET request to the Frontend app of type:

   ``<frontend-preview-url>/<signature>/<page-id>/<revision-id>``
-  The Frontend app verifies the signature and returns an error if it’s not valid
-  The Frontend app uses the ``page-id`` and the ``revision-id`` to make a call to
   the Publishing Tool to get the preview content using the :ref:`content-preview-api`.
-  The Frontend app renders the preview content

Signature
---------

The signature in the preview url is an `HMAC(K, m)`_ where:

-  *K*: a private key shared between the Publishing Tool and the Frontend app
-  *m*: is the message ``'<page-id>/<revision-id>/'``



.. _Publishing Tool app: https://github.com/nhsuk/nhsuk-content-store
.. _Frontend app: https://github.com/nhsuk/betahealth
.. _Authentication section: http://nhsuk-content-store.readthedocs.io/en/latest/references.html
.. _HMAC(K, m): https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
