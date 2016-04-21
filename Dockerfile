#
# Docker image for graph-tool server
#
# - This creates plain Python 2.x server with graph-tool and flask to 
#   implement graph processing web API.
#
FROM debian:jessie

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

RUN apt-get update && apt-get install -y apt-transport-https

# For installing graph-tool
RUN mkdir /graph-tool
WORKDIR /graph-tool
ADD . /graph-tool

RUN echo "deb http://downloads.skewed.de/apt/jessie jessie main" >>/etc/apt/sources.list
RUN echo "deb-src http://downloads.skewed.de/apt/jessie jessie main" >>/etc/apt/sources.list
RUN apt-key add graph-tool-pub-key.txt

# Install OS-level packages and misc. tools
RUN apt-get update
RUN apt-get install -y curl python-graph-tool

# Install Python dependencie
RUN curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python2
RUN pip install flask flask-restful

# Add directory for REST API server code
RUN mkdir /app
WORKDIR /app

ADD . /app

EXPOSE 5000

# Run API server
CMD ["python", "api/api.py"]
