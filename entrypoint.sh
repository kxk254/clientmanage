#!/bin/bash
set -e

cd /clientmanage

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Fixing permissions..."
chown -R 101:101 /clientmanage/staticfiles /clientmanage/media

echo "Starting Gunicorn..."
exec gunicorn cm.wsgi:application --bind 0.0.0.0:8000