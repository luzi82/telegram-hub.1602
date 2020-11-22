FROM debian:10.6

# Install custom tools, runtimes, etc.
# For example "bastet", a command-line tetris clone:
# RUN brew install bastet
#
# More information: https://www.gitpod.io/docs/config-docker/

USER root

# install python
RUN true \
 && apt-get update \
 && apt-get install -y \
    python3.7 \
    python3-venv

# install curl
RUN true \
 && apt-get update \
 && apt-get install -y \
    curl

# install nodejs
RUN true \
 && curl -sL https://deb.nodesource.com/setup_14.x | bash - \
 && apt-get update \
 && apt-get install -y \
    nodejs
