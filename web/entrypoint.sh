#!/bin/bash

python3 manage.py migrate
gunicorn ReNgGinaNg.wsgi:application --bind 0.0.0.0:8000 --workers 4 --limit-request-line 8190

exec "$@"
