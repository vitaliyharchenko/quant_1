cd ~/Dev/Django/physenv
source bin/activate
cd ~/Dev/Django/physicum

psql
CREATE USER physuser WITH PASSWORD '$$$$';
CREATE DATABASE physdb OWNER physuser;
ALTER USER physuser CREATEDB;

pip install psycopg2
pip install django-markdown
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

pip freeze > requirements.txt


# обнуление БД

```
sudo su postgres -c 'pg_ctl -D /opt/local/var/db/postgresql84/defaultdb/ restart' (рестарт psql)
psql
DROP DATABASE physdb;
CREATE DATABASE physdb OWNER physuser;
ALTER USER physuser CREATEDB;
python manage.py makemigrations users
python manage.py migrate
python manage.py createsuperuser
create user - harchenko.grape@gmail.com, Oleinik1
```

# Развертываем фронтенд #
```
npm install --save-dev gulp - в директории проекта
npm init
npm
npm install bootstrap@4.0.0-alpha.3
```


b tot
