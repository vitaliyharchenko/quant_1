Quant.zone
==========

Наше LMS приложение

**Requirements for local development:** Python 3.4, PostgreSQL, Gulp, NodeJS

**Requirements for python:** requirements.txt

**Requirements for frontend:** package.json

## Init:

1. Git clone

    ```
    https://github.com/vitaliyharchenko/quantzone.git
    ```

2. For local development create copy of quantzone/settings_dev.py named settings_local.py

    ```
    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    DEBUG = True
    CURRENT_HOST = 'http://127.0.0.1:8000'
    ALLOWED_HOSTS = ['http://127.0.0.1:8000']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'qdb',
            'HOST': 'localhost',
            'PASSWORD': '***',
         'USER': 'quser',
      }
    }

    STATIC_URL = '/static/'
    STATIC_ROOT = '/static/'
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )
    ```

### Frontend:

1. Load requirements

    ```
    npm install
    ```

2. Start Gulp

    ```
    gulp
    ```

3. That's it -- you're done!


### Backend:

1. Create and activate virtualenv

    ```
    virtualenv qenv --python=python3.4
    source quenv/bin/activate
    ```

2. Load requirements

    ```
    pip install -r requirements.txt
    ```

3. Create database

    ```
    sudo su - postgres
    psql
    create user "quser" with password '***';
    create database "qdb" owner "quser";
    alter user quser createdb;
    grant all privileges on database qdb TO quser;
    ```

4. Create data structure for django

    ```
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

5. Load all data from .json file

    ```
    python manage.py loaddata db.json
    ```

6. Save all data to .json file

    ```
    python manage.py dumpdata --exclude contenttypes > db.json
    ```

## Deploy process

1. Connect to server
    ```
    ssh-keygen -R 188.93.211.161
    ssh root@188.93.211.161
    aw!Biiug16Z3X2
    ```
    
2. Upgrade Ubuntu
    ```
    sudo apt-get update
    sudo apt-get upgrade
    ```
   
3. Language settings    

    ````
    locale-gen ru_RU.UTF-8
    sudo nano /etc/default/locale
    * LANG="ru_RU.UTF-8"
    * LC_ALL="ru_RU.UTF-8"
    ```

4. Install system packages
    
    ```
    sudo apt-get install python3-pip
    sudo apt-get install libpq-dev python3.4-dev
    sudo apt-get install python-virtualenv git nginx postgresql postgresql-contrib
    sudo apt-get install libfreetype6 libfreetype6-dev
    sudo apt-get install libjpeg8 libjpeg62-dev
    sudo apt-get install python-imaging
    ```

5. Init database structure
    
    ```
    sudo su - postgres
    psql
    create user "quser" with password '4203';
    create database "qdb" owner "quser";
    alter user quser createdb;
    grant all privileges on database qdb TO quser;
    \q
    su - root
    ```

6. Clone git project

    ```
    cd /opt
    git clone https://github.com/vitaliyharchenko/quantzone.git
    ```

7. Create? activate and set virtualenv

    ```    
    virtualenv /opt/qenv --python=python3.4
    source /opt/qenv/bin/activate
    cd /opt
    git clone https://github.com/vitaliyharchenko/quantzone.git
    pip3 install -r /opt/quantzone/requirements.txt
    pip3 install uwsgi
    ```

8. Make Django migrations
       
    ```
    cd /opt/quantzone
    python manage.py collectstatic
    python manage.py makemigrations users teaching
    python manage.py migrate
    python manage.py createsuperuser
    ```

9. Run Django and connect by port

    ```    
    python manage.py runserver 0.0.0.0:8000
    go to http://quant.zone:8000
    ```

the web client <-> Django | works

10. Run Django by uWSGI in virtualenv

    ```    
    uwsgi --http :8000 --module quantzone.wsgi
    go to http://quant.zone:8000
    ```
the web client <-> uWSGI <-> Django | works

11. Run Django by uWSGI globally

    ```
    uwsgi --http :8000 --chdir /opt/quantzone --module quantzone.wsgi --virtualenv /opt/qenv
    go to http://quant.zone:8000
    ```
    
the web client <-> uWSGI <-> Django | works

12. Check nginx work

    ```
    go to http://quant.zone
    ```

the web client <-> the web server |works

13. Set up nginx

    ````
    sudo nano /etc/nginx/sites-available/quantzone
    cd /etc/nginx/sites-enabled
    sudo ln -s ../sites-available/quantzone
    sudo rm default
    sudo service nginx restart
    
    go to http://quant.zone/static/css/main.css
    ```
    
Nginx serving static and media correctly

14. Set up sockets

    ```
    sudo nano /etc/nginx/sites-available/quantzone (uncomment socket in nginx)
    uwsgi --socket :8001 --wsgi-file test.py --chmod-socket=664
    
    sudo chmod -R 777 quantzone.sock
    uwsgi --socket quantzone.sock --wsgi-file test.py --chmod-socket=666
    
    go to http://quant.zone
    ```

the web client <-> the web server <-> the socket <-> uWSGI <-> Python | works correctly

15. Run server by .ini file in virtualenv and globally

    ```
    uwsgi --ini uwsgi.ini
    
    deactivate
    pip3 install uwsgi
    ```

16. Create vassals for serving several versions of product together

    ```
    sudo mkdir /opt/uwsgi
    sudo mkdir /opt/uwsgi/vassals
    
    sudo ln -s /opt/quantzone/uwsgi.ini /opt/uwsgi/vassals/
    
    sudo uwsgi --emperor /opt/uwsgi/vassals --uid www-data --gid www-data
    ```

17. Set auto reloading of vassals
    
    ```
    nano /etc/rc.local
    
    перед строкой “exit 0” добавляем:
    /usr/local/bin/uwsgi --emperor /opt/uwsgi/vassals --uid www-data --gid www-data
    ```

18. Final settings of nginx

    ```    
    change port nginx to 80
    ```