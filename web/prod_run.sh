#!/bin/bash

/usr/bin/python3.5 /data/web/quantzone/manage.py makemigrations blocks courses events groups lms nodes organizations places results tasks testing users
/usr/bin/python3.5 /data/web/quantzone/manage.py migrate
/usr/bin/python3.5 /data/web/quantzone/manage.py collectstatic
/usr/bin/python3.5 /data/web/quantzone/manage.py loaddata /data/web/quantzone/fixtures/db_final.json