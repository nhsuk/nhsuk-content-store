Start
-----

1. `$ docker-compose build`
2. `$ docker-compose up`
3. In another terminal session:
    - Run DB migrations: `$ docker-compose exec wagtail ./manage.py migrate`
    - Create superuser: `$ docker-compose exec wagtail ./manage.py createsuperuser`
4. Visit [http://localhost:8000/]()
