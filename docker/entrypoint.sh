#!/bin/sh

set -o errexit
set -o nounset

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000