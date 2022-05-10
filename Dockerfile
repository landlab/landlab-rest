FROM mambaorg/micromamba:0.23.0

ARG MAMBA_USER=mambauser
ARG MAMBA_USER_ID=1000
ARG MAMBA_USER_GID=1000
ENV MAMBA_USER=$MAMBA_USER

USER root

COPY --chown=$MAMBA_USER:$MAMBA_USER env.yaml /tmp/env.yaml
RUN micromamba install -y -f /tmp/env.yaml && micromamba clean --all --yes
ARG MAMBA_DOCKERFILE_ACTIVATE=1

# File Author / Maintainer
MAINTAINER Eric Hutton

# RUN export PATH=/usr/local/python/bin:$PATH

# install landlab-rest package
ADD . /landlab-rest
RUN pip install /landlab-rest
RUN cd /landlab-rest/grid-sketchbook-master

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /landlab-rest

# Set the default command to execute
# when creating a new container
CMD start-sketchbook
