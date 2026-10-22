#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  . .venv/bin/activate
fi

python manage.py migrate --noinput
python manage.py seed_demo || echo "WARNING: seed_demo failed, continuing startup"
python manage.py collectstatic --noinput
gunicorn config.wsgi:application -c gunicorn.conf.py
