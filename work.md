IP адрес	188.93.211.161

ssh-keygen -R 188.93.211.161
ssh root@188.93.211.161
aw!Biiug16Z3X2
sudo apt-get update
sudo apt-get upgrade

locale-gen ru_RU.UTF-8
sudo nano /etc/default/locale
* LANG="ru_RU.UTF-8"
* LC_ALL="ru_RU.UTF-8"

sudo apt-get install python3-pip
sudo apt-get install libpq-dev python3.4-dev
sudo apt-get install python-virtualenv git nginx postgresql postgresql-contrib

sudo su - postgres
psql
create user "quser" with password '4203';
create database "qdb" owner "quser";
alter user quser createdb;
grant all privileges on database qdb TO quser;
\q
su - root

virtualenv /opt/qenv --python=python3.4
source /opt/qenv/bin/activate
cd /opt
git clone https://github.com/vitaliyharchenko/quantzone.git
pip3 install -r /opt/quantzone/requirements.txt
pip3 install uwsgi

cd /opt/quantzone
python manage.py collectstatic
python manage.py makemigrations users teaching
python manage.py migrate
python manage.py createsuperuser

python manage.py runserver 0.0.0.0:8000
http://quant.zone:8000

uwsgi --http :8000 --module quantzone.wsgi
http://quant.zone:8000

sudo nano /etc/nginx/sites-available/quantzone
cd /etc/nginx/sites-enabled
sudo ln -s ../sites-available/quantzone
sudo rm default
sudo service nginx restart

go to http://quant.zone/static/css/main.css
Nginx serving static and media correctly

uncomment socket in nginx
sudo chown -R root:www-data quantzone
nano /var/log/nginx/error.log


sudo pip3 install virtualenvwrapper
sudo pip install uwsgi
sudo pip3 install uwsgi

sudo service uwsgi start




uwsgi --ini uwsgi.ini

uwsgi --socket quantzone.sock --wsgi-file test.py --chmod-socket=664


uwsgi --socket quantzone.sock --module quantzone.wsgi --chmod-socket=664












apt-get install python3-pip
apt-get install libpq-dev python3.4-dev python-virtualenv git nginx postgresql postgresql-contrib
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
git clone https://github.com/vitaliyharchenko/quantzone.git
pip3 install -r /opt/quantzone/requirements.txt
pip3 install uwsgi


'''
'''