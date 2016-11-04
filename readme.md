[![Dependency Status](https://gemnasium.com/badges/github.com/nhsuk/nhsuk-content-store.svg)](https://gemnasium.com/github.com/nhsuk/nhsuk-content-store)

# NHS.UK Content Store

Content Store for NHS.UK

## Dependencies

* python 3 (tested on 3.5.2)
* postgres (tested on 9.4+)
* [docker](https://www.docker.com) if used

## Development installation

### Without Docker

1. Clone the repository:

  ```
  git clone https://github.com/nhsuk/nhsuk-content-store
  cd nhsuk-content-store
  ```

2. Install `virtualenv` if you don't have it already:

  ```
  pip install virtualenv
  ```

3. Create and activate the virtualenv

  ```
  virtualenv --python=python3 env
  source env/bin/activate
  pip install -U pip
  ```

4. Install the dependencies

  ```
  pip install -r requirements/dev.txt
  ```

5. Create a `local.py` settings file (it's gitignored by default) in case you need to override things:

  ```
  cp nhsuk/settings/local.py.example nhsuk/settings/local.py
  ```

6. Create the db

  By default, the dev version uses postgres, if you want, you can switch to sqlite by uncommenting the
  related lines in your `local.py` file.

    ```
    psql -p5432
    create database nhsuk;
    ```

7. Configure the db

  ```
  ./manage.py migrate
  ./manage.py createsuperuser
  ```

8. Start the server

  ```
  ./manage.py runserver
  ```

9. Visit [http://127.0.0.1:8000/admin/]() and log in using the username/password chosen when running `createsuperuser`

### With Docker

1. Clone the repository:

  ```
  git clone https://github.com/nhsuk/nhsuk-content-store
  cd nhsuk-content-store
  ```

2. Build the image:

  ```
  docker-compose build
  ```
3. Start the container

  ```
  docker-compose up
  ```

4. Configure the db

  In another terminal session:

  ```
  docker-compose exec content-store ./manage.py migrate
  docker-compose exec content-store ./manage.py createsuperuser
  ```

5. Visit [http://localhost:8000/admin]() and log in using the username/password chosen when running `createsuperuser`


## Contributing

1. Make sure you configure your editor to use the flake8 config file `setup.cfg`

2. To run the unit tests:

  ```
  ./manage.py test
  ```

3. Make sure you isort your imports before committing:

  ```
  isort -rc .
  ```


## Heroku

The app is ready to be deployed to Heroku for testing purposes, Heroku shouldn't be used prod with this setup.

By default, the assets are stored/retrieved from Heroku whilst the uploaded images are stored/retrieved from Azure Storage.

Heroku specific files:

* `requirements.txt`: which includes `requirements/heroku.txt`
* `nhsuk/settings/heroku.py`: heroku settings file
* `nhsuk/heroku_wsgi.py`: heroku wsgi file
