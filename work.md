IP адрес	188.93.211.161

ssh-keygen -R 188.93.211.161
ssh root@188.93.211.161
aw!Biiug16Z3X2
sudo apt-get update
sudo apt-get upgrade
apt-get install python3-pip
sudo apt-get install libpq-dev
sudo apt-get install python3.4-dev
sudo apt-get install python-virtualenv git nginx postgresql postgresql-contrib
locale-gen ru_RU.UTF-8

sudo su - postgres
psql
create user "quser" with password '4203';
create database "qdb" owner "quser";
alter user quser createdb;
grant all privileges on database qdb TO quser;
\q
su - root

sudo virtualenv /opt/qenv --python=python3.4
source /opt/qenv/bin/activate
cd /opt
git clone https://github.com/vitaliyharchenko/quant.zone.git
pip3 install -r /opt/quant.zone/requirements.txt
pip3 install uwsgi


cd /opt/quant.zone
uwsgi --http :8000 --wsgi-file test.py
go to quant.zone:8000
the web client <-> uWSGI <-> Python

python manage.py collectstatic
python manage.py makemigrations teaching users
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000
go to quant.zone:8000
uwsgi --http :8000 --module quantzone.wsgi
go to quant.zone:8000
the web client <-> uWSGI <-> Django | works
go to quant.zone
the web client <-> the web server |works


sudo ln -s ~/opt/quant.zone/nginx.conf /etc/nginx/sites-enabled/
cd /etc/nginx/sites-enabled
sudo rm default
sudo /etc/init.d/nginx restart

go to http://quant.zone:8000/dist/css/main.css
Nginx serving static and media correctly

apt-get install uwsgi-core
pip3 install uwsgi

uwsgi --http :8000 --wsgi-file test.py
go to http://188.93.211.161:8000
the web client <-> the web server <-> the socket <-> uWSGI <-> Python | works correctly

uwsgi --socket quantzone.sock --wsgi-file test.py --chmod-socket=666
go to http://quant.zone:8000
socket works correctly

uwsgi --socket quantzone.sock --module quantzone.wsgi --chmod-socket=666

uwsgi --ini quantzone_uwsgi.ini
uwsgi --stop quantzone_uwsgi.ini