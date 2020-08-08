# This Dockerfile is expected to be used with docker-compose.yml from ackrep_deployment

# Note: current directory (.) is specified by `context` in `docker-compose.yml`

FROM python:3.7-slim

LABEL ackrep.container.name="ackrep-django"

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}


# turn on root access inside the container (for debugging only) !!
# RUN echo 'root:Docker!' | chpasswd

# Install packages needed to run your application (not build deps):
#   mime-support -- for mime types when serving static files
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    mime-support \
    lsof \
    git \
    sudo \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && usermod -a -G sudo ${APP_USER} \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
ADD ./ackrep_core/requirements.txt /requirements.txt
ADD ./ackrep_core/deployment_requirements.txt /deployment_requirements.txt

# OR, if you're using a directory for your requirements, copy everything (comment out the above and uncomment this if so):
# ADD requirements /requirements

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.

# also install docker in this step (before removing the whole stuff)
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /requirements.txt \
    && pip install --no-cache-dir -r /deployment_requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS

RUN set -ex \
    && DOCKER_DEPS=" \
    apt-transport-https  curl  software-properties-common gnupg2 \
    " \
    && apt-get install -y --no-install-recommends $DOCKER_DEPS \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add - \
    && add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
    
    
RUN set -ex \
    && apt-get update \
    && apt-cache policy docker-ce \
    && apt-get install -y docker-ce \
    && rm -rf /var/lib/apt/lists/*

    
# TODO: move the apt-get purge command to the end of the apt section

# this enables the usage of ipython inside the container (useful for debugging)
RUN mkdir -p /home/$APP_USER
RUN chown ${APP_USER}:${APP_USER} /home/$APP_USER

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir -p /work/ackrep_core
ADD ./ackrep_core /work/ackrep_core
RUN chown -R ${APP_USER}:${APP_USER} /work
WORKDIR /work/ackrep_core

# ensure that we have no legacy db file lurking around from local testing
RUN rm -f db.sqlite3
RUN rm -f /work/ackrep_core/media/*

RUN mkdir /work/ackrep_data
ADD ./ackrep_data /work/ackrep_data
RUN chown -R ${APP_USER}:${APP_USER} /work/ackrep_data

ADD ./ackrep_deployment/dockerfiles/ackrep_core/additional_files /work/




# add the most important python packages for the demo-instance
#  TODO: !! This should be handled via Environment specifications:

ADD ./ackrep_deployment/dockerfiles/ackrep_data/additional_files /work/
RUN pip install --no-cache-dir -r /work/tmp_requirements.txt

# TODO: move this up near the docker install
RUN pip install --no-cache-dir docker-compose

COPY ./ackrep_deployment/docker-compose.yml /work/


# uWSGI will listen on this port
EXPOSE 8000

# Add any static environment variables needed by Django or your settings file here:
ENV DJANGO_SETTINGS_MODULE=ackrep_core_django_settings.settings

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
RUN DATABASE_URL='' python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=ackrep_core_django_settings/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_HTTP=:8000 UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=2 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
ENV UWSGI_STATIC_MAP="/static/=/work/ackrep_core/static/" UWSGI_STATIC_EXPIRES_URI="/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"

# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
# this will be run every time when the container starts
ENTRYPOINT ["/work/docker-entrypoint.sh"]


# this is the default command and will be run after the entrypoint script (due to `exec "$@"` at the end of that script)
# Start uWSGI
CMD ["uwsgi", "--show-config"]
