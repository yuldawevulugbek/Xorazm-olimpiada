#!/usr/bin/env bash
set -euo pipefail

if [ -d ".venv" ]; then
  . .venv/bin/activate
fi

# Render'da PostgreSQL ulanmagan bo'lsa ishga tushmaymiz: SQLite har deployda o'chib,
# o'quvchilar va natijalar yo'qolib ketadi.
if [ -n "${RENDER:-}" ] && [ -z "${DATABASE_URL:-}" ]; then
  echo "ERROR: DATABASE_URL yo'q. Render'da PostgreSQL bazasini ulang (render.yaml shuni avtomatik qiladi)." >&2
  exit 1
fi

python manage.py migrate --noinput
python manage.py seed_demo || echo "WARNING: seed_demo failed, continuing startup"
python manage.py collectstatic --noinput
gunicorn config.wsgi:application -c gunicorn.conf.py
