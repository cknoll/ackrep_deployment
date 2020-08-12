#!/bin/sh
set -e


# this environment variable will be set by docker-compose
if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then

    # create an empty database
    python $MAIN_DIR/ackrep_core/manage.py migrate --noinput --run-syncdb
    # ackrep -l ../ackrep_data
    python -c "from ackrep_core import core; core.load_repo_to_db('$MAIN_DIR/ackrep_data')"
    # this is the place where fixtures could be loaded
fi


if [ "x$INIT_RUNNERS" = 'xon' ]; then

    echo "start runner containers in standby"
    ackrep --init-containers

fi

exec "$@"
