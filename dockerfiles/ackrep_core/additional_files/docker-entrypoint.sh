#!/bin/sh
set -e


if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then

    # create an empty database
    python manage.py migrate --noinput --run-syncdb

    # this is the place where fixtures could be loaded

fi

exec "$@"
