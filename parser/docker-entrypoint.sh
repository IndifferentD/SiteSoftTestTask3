#!/bin/sh

set -e
/usr/src/habr_parser/wait-for-it.sh parser_db:5432 -t 30

exec "$@"