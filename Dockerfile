#
# Docker image for graph-tool server
#
# - This creates plain Python 3.x server with graph-tool and flask to
#   implement graph processing web API.
#
FROM ubuntu:yakkety
MAINTAINER Keiichiro Ono <kono@ucsd.edu>

# Install Flask related packages for Python 3
RUN apt-get update && apt-get install -y apt-transport-https python-pip
RUN pip install flask flask-restful

# For installing graph-tool
RUN mkdir /graph-tool
WORKDIR /graph-tool
ADD . /graph-tool

RUN echo "deb http://downloads.skewed.de/apt/yakkety yakkety universe" >>/etc/apt/sources.list
RUN echo "deb-src http://downloads.skewed.de/apt/yakkety yakkety universe" >>/etc/apt/sources.list
RUN apt-key add graph-tool-pub-key.txt

# Install OS-level packages and misc. tools
RUN apt-get update
RUN apt-get install -y python-graph-tool

# Install Python dependencie
# RUN curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python2

# Add directory for REST API server code
RUN mkdir /app
WORKDIR /app

ADD . /app
RUN mkdir /app/images

EXPOSE 5000

RUN python --version
# Run API server
CMD ["python", "api/api.py"]
