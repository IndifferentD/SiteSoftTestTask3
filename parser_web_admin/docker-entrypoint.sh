#!/bin/sh

set -e
/usr/src/parser_web_admin/wait-for-it.sh parser_db:5432 -t 30
cd /usr/src/parser_web_admin
python manage.py migrate
exec "$@"