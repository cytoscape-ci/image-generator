#
# Docker image for VIZBI 2015 Tutorial
#
# This is a generic setup for network data analysis and visualization.
# This Distribution includes:
#  - Python
#  - IPython Notebook
#  - Standard data analysis tools, including SciPy and NumPy
#  - NetworkX, igraph, and graph-tool
#
FROM debian:jessie

MAINTAINER Keiichiro Ono <kono@ucsd.edu>

# For installing graph-tool
RUN mkdir /graph-tool
WORKDIR /graph-tool
ADD . /graph-tool

RUN echo "deb http://downloads.skewed.de/apt/jessie jessie main" >>/etc/apt/sources.list
RUN echo "deb-src http://downloads.skewed.de/apt/jessie jessie main" >>/etc/apt/sources.list
RUN apt-key add graph-tool-pub-key.txt

# Install OS-level packages and misc. tools
RUN apt-get update && apt-get install -y python-graph-tool

# Install Python dependencie
RUN apt-get install -y curl
RUN curl -fSL 'https://bootstrap.pypa.io/get-pip.py' | python2

RUN pip install jupyter flask flask-restful

RUN mkdir /app
WORKDIR /app

ADD . /app

EXPOSE 5000

CMD ["python", "api/api.py"]
