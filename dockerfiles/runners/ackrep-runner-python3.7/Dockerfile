# Dockerfile for the runner: ackrep-runner-python3.7

FROM ackrep_base


LABEL ackrep.image.name="ackrep-runner-python37"
LABEL ackrep.image.entity_key="YJBOX"
LABEL ackrep.image.type="runner"


# make the container id (which is stored in the hostname) known to other containers


# Copy in your requirements file
RUN mkdir -p /tmp
COPY ./ackrep_deployment/dockerfiles/runners/ackrep-runner-python3.7/additional_files /tmp
WORKDIR $RUNNER_DIR

RUN ls /tmp


# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step.
# Correct the path to your production requirements file, if needed.


RUN set -ex \
    && BUILD_DEPS=" \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && pip install --no-cache-dir -r /tmp/runner_requirements.txt \
    \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*



# Change to a non-root user
# (this might be disabled for to simplify development (allow writing to volumes, which do not yet exist at build time))
USER ${RUNNER_USER}:${ACKREP_GROUP}

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

CMD ["/bin/bash"]
