|Build Status| |Dependency Status| |Coverage Status| |Documentation Status|

NHS.UK Content Store
====================

Content Store for NHS.UK.

The full documentation is on `Read the Docs <http://nhsuk-content-store.readthedocs.io/en/latest/>`_

Dependencies
------------

-  python 3 (tested on 3.5.2)
-  postgres (tested on 9.4+)
-  `docker`_ if used

Development installation
------------------------

Without Docker
~~~~~~~~~~~~~~

#. Clone the repository::

    git clone https://github.com/nhsuk/nhsuk-content-store
    cd nhsuk-content-store

#. Install ``virtualenv`` if you don’t have it already::

    pip install virtualenv

#. Create and activate the virtualenv::

    virtualenv --python=python3 env
    source env/bin/activate
    pip install -U pip

#. Install the dependencies::

    pip install -r requirements/dev.txt

#. Create a ``local.py`` settings file (it’s gitignored by default) in
   case you need to override things::

    cp nhsuk/settings/local.py.example nhsuk/settings/local.py

#. Create the db. By default, the dev version uses postgres, if you want, you can switch to sqlite by uncommenting the related lines in your ``local.py`` file::

    psql -p5432
    create database nhsuk;

#. Configure the db::

    ./manage.py migrate
    ./manage.py createsuperuser

#. Start the server::

    ./manage.py runserver

#. Visit `http://127.0.0.1:8000/admin/`_ and log in using the
   username/password chosen when running ``createsuperuser``

With Docker
~~~~~~~~~~~

#. Clone the repository::

    git clone https://github.com/nhsuk/nhsuk-content-store
    cd nhsuk-content-store

#. Build the image::

    docker-compose build

#. Start the container::

    docker-compose up

#. Configure the db. In another terminal session::

    docker-compose exec content-store ./manage.py migrate
    docker-compose exec content-store ./manage.py createsuperuser

#. Visit `http://localhost:8000/admin`_ and log in using the
   username/password chosen when running ``createsuperuser``

Contributing
------------

#. Make sure you configure your editor to use the flake8 config file
   ``setup.cfg``

#. To run the unit tests::

    ./manage.py test

#. Make sure you isort your imports before committing::

    isort -rc .

#. Make sure you run lint before committing::

    flake8 .

Heroku
------

The app is ready to be deployed to Heroku for testing purposes, Heroku
shouldn’t be used prod with this setup.

By default, the assets are stored/retrieved from Heroku whilst the
uploaded images are stored/retrieved from Azure Storage.

Heroku specific files:

-  ``requirements.txt``: which includes ``requirements/heroku.txt``
-  ``nhsuk/settings/heroku.py``: heroku settings file
-  ``nhsuk/heroku_wsgi.py``: heroku wsgi file
-  ``bin/post_compile``: heroku post deploy file that runs the django migrate command automatically after each deploy

.. _docker: https://www.docker.com
.. _`http://127.0.0.1:8000/admin/`:
.. _`http://localhost:8000/admin`:

.. |Build Status| image:: https://travis-ci.org/nhsuk/nhsuk-content-store.svg?branch=master
   :target: https://travis-ci.org/nhsuk/nhsuk-content-store
.. |Dependency Status| image:: https://gemnasium.com/badges/github.com/nhsuk/nhsuk-content-store.svg
   :target: https://gemnasium.com/github.com/nhsuk/nhsuk-content-store
.. |Coverage Status| image:: https://coveralls.io/repos/github/nhsuk/nhsuk-content-store/badge.svg?branch=master
   :target: https://coveralls.io/github/nhsuk/nhsuk-content-store?branch=master
.. |Documentation Status| image:: https://readthedocs.org/projects/nhsuk-content-store/badge/?version=latest
   :target: http://nhsuk-content-store.readthedocs.io/en/latest/?badge=latest
