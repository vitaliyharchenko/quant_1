Quant.zone
==========

Quant.zone
==========

Наше LMS приложение

**Requirements for local development:** Python 3.6, PostgreSQL, Gulp, NodeJS, Graphviz

## Local dev:

1. Git clone

    ```
    ssh root@188.127.249.128
    oGWRAKrle8so
    git clone -b v1.1.0 https://github.com/vitaliyharchenko/quantzone.git
    ```

2. [Install Docker on Ubuntu 16.04 x64](https://docs.docker.com/engine/installation/linux/ubuntu/)

3. [Install Docker Compose](https://docs.docker.com/compose/install/)

4. Create data structure for django

    ```
    docker-compose run web python3 manage.py makemigrations
    docker-compose run web python3 manage.py migrate
    docker-compose run web python3 manage.py createsuperuser
    ```

5. Load all data from .json file

    ```
    python manage.py loaddata db.json
    ```

6. Save all data to .json file and load locally

    ```
    python manage.py dumpdata --exclude contenttypes > fixtures/db.json
    scp root@188.93.211.161:/opt/quantzone/fixtures/db.json /Users/vitaliyharchenko/Dev/quantzone
    ```

### Advices

1. Work in coding style: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/
