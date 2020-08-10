# Dockerfile for the runner: ackrep-runner-python3.7

FROM ackrep_base


LABEL ackrep.container.name="ackrep-runner-python37"


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
COPY ./ackrep_deployment/dockerfiles/runners/ackrep-runner-python3/additional_files $RUNNER_DIR
WORKDIR $RUNNER_DIR

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


# tmp (obsolete after next complete rebuild)

RUN mkdir -p $RUNNER_DIR/container \
    && mkdir -p $RUNNER_DIR/jobs \
    && chown -R ${ACKREP_USER}:${ACKREP_GROUP} $RUNNER_DIR \
    # do not allow group to write -> 775
    && chmod -R 775 $RUNNER_DIR \
    && echo


# Change to a non-root user
# (this might be disabled for to simplify development (allow writing to volumes, which do not yet exist at build time))
USER ${RUNNER_USER}:${ACKREP_GROUP}


# make the container id (which is stored in the hostname) known to other containers
RUN echo $(hostname) > $RUNNER_DIR/container/$(hostname).txt

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["/bin/bash"]
