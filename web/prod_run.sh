#!/bin/bash

/usr/bin/python3.5 /data/web/quantzone/manage.py makemigrations
/usr/bin/python3.5 /data/web/quantzone/manage.py migrate
/usr/bin/python3.5 /data/web/quantzone/manage.py collectstatic
#/usr/bin/python3.5 /data/web/quantzone/manage.py loaddata /data/web/db.json