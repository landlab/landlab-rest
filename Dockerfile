############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Eric Hutton

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(. /etc/lsb-release && printf '%s' $DISTRIB_CODENAME) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl vim dialog net-tools build-essential lsb-release

# Install Python and Basic Python Tools
RUN curl https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh > miniconda.sh
RUN /bin/bash ./miniconda.sh -b -f -p /usr/local/python
RUN export PATH=/usr/local/python/bin:$PATH
RUN /usr/local/python/bin/conda config --add channels conda-forge
RUN /usr/local/python/bin/conda config --add channels landlab

# Copy the application folder inside the container
ADD . /landlab-rest

# Get pip to download and install requirements:
RUN /usr/local/python/bin/conda install --yes --file=/landlab-rest/requirements.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /landlab-rest

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD /usr/local/python/bin/python server.py
