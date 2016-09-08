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

ЗАпускаем сервер на uwsgi

'''
source /opt/qenv/bin/activate
pip3 install uwsgi

uwsgi --http :8000 --wsgi-file test.py
$$$WORKS$$$

python manage.py runserver 0.0.0.0:8000
$$$WORKS$$$

uwsgi --http :8000 --module quantzone.wsgi
$$$WORKS$$$

sudo ln -s ~/opt/quant.zone/quantzone_nginx.conf /etc/nginx/sites-enabled/
python manage.py collectstatic
sudo /etc/init.d/nginx restart

http://quant.zone:8000/media/media.png
http://quant.zone:8000/dist/css/main.css
'''