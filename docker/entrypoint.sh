#!/bin/sh
# Apply pending migrations and refresh static files on every start.
set -e
python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
