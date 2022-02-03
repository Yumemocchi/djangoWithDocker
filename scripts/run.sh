#!/bin/sh

set -e

python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

gunicorn --workers 4 --bind 0.0.0.0:8000 blog.wsgi