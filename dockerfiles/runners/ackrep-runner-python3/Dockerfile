# Dockerfile for the runner: ackrep-runner-python3.7

FROM ackrep_base


LABEL ackrep.image.name="ackrep-runner-python37"
LABEL ackrep.image.entity_key="YJBOX"
LABEL ackrep.image.type="runner"


# make the container id (which is stored in the hostname) known to other containers

RUN mkdir -p $RUNNER_DIR/container/$(hostname)

# Copy in your requirements file
COPY ./ackrep_deployment/dockerfiles/runners/ackrep-runner-python3/additional_files $RUNNER_DIR/container/$(hostname)
WORKDIR $RUNNER_DIR/container/$(hostname)

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.
RUN set -ex \
    && BUILD_DEPS=" \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r runner_requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*


# RUN set -ex \
#     && BUILD_DEPS=" \
#     build-essential \
#     " \
#     && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
#     && pip install --no-cache-dir -r runner_requirements.txt \
#     \
#     && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
#     && rm -rf /var/lib/apt/lists/*

#
# # tmp (obsolete after next complete rebuild)
#
# RUN mkdir -p $RUNNER_DIR/container \
#     && mkdir -p $RUNNER_DIR/jobs \
#     && chown -R ${ACKREP_USER}:${ACKREP_GROUP} $RUNNER_DIR \
#     # do not allow group to write -> 775
#     && chmod -R 775 $RUNNER_DIR \
#     && echo
#
#
# # copy stuff
# COPY --from=ackrep_core $MAIN_DIR/ackrep_core $MAIN_DIR/ackrep_core
#
# WORKDIR $MAIN_DIR/ackrep_core
# RUN pip install -e .


# Change to a non-root user
# (this might be disabled for to simplify development (allow writing to volumes, which do not yet exist at build time))
USER ${RUNNER_USER}:${ACKREP_GROUP}

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["/bin/bash"]
