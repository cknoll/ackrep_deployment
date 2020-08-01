#!/bin/sh
set -e


if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then

    # create an empty database
    python manage.py migrate --noinput --run-syncdb
    # ackrep -l ../ackrep_data
    python -c "from ackrep_core import core; core.load_repo_to_db('/code/ackrep_data')"

    # this is the place where fixtures could be loaded

fi

exec "$@"
