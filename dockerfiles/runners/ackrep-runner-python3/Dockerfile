# Dockerfile for the runner: ackrep-runner-python3

# Note: current directory (.) is specified by `context` in `docker-compose.yml`

FROM python:3.7-slim

LABEL ackrep.container.name="ackrep-runner-python37"

# Create a group and user to run our app
ARG APP_USER=appuser
RUN groupadd -r ${APP_USER} && useradd --no-log-init -r -g ${APP_USER} ${APP_USER}


# turn on root access inside the container (for debugging only) !!
# RUN echo 'root:Docker!' | chpasswd

# Install packages needed to run your application (not build deps):
# We need to recreate the /usr/share/man/man{1..8} directories first because
# they were clobbered by a parent image.
RUN set -ex \
    && RUN_DEPS=" \
    git \
    " \
    && seq 1 8 | xargs -I{} mkdir -p /usr/share/man/man{} \
    && apt-get update && apt-get install -y --no-install-recommends $RUN_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Copy in your requirements file
RUN mkdir -p /ackrep_runner
COPY ./ackrep_deployment/dockerfiles/runners/ackrep-runner-python3/additional_files /ackrep_runner/
WORKDIR /ackrep_runner

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    build-essential \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r runner_requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# this is needed for the usage of ipython inside the container (useful for debugging)
RUN mkdir -p /home/$APP_USER
RUN chown ${APP_USER}:${APP_USER} /home/$APP_USER


# Change to a non-root user
USER ${APP_USER}:${APP_USER}

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["/bin/bash"]
