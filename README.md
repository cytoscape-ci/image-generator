# graph-image-generator

## Introduction
This is a service to generate network (graph) diagram from CX JSON.

## Quick Start Guide
 
1. ```git clone https://github.com/cytoscape-ci/graph-image-generator.git```
1. ```cd graph-image-generator```
1. ```docker build -t cytoscape-ci/graph-image-generator .```
1. ```docker run -p 5000:5000 cytoscape-ci/graph-image-generator```

----

## REST API Reference

### ```/```

#### Supported methods 
* **GET**

#### Description
Returns basic information of this service.

#### Sample Output
```json
{
    name: "graph-image-generator",
    version: "v1",
    build: "2-19-2016",
    description: "Network image generator service. This service generates network images on the fly from any CX JSON.",
    documents: "https://github.com/cytoscape-ci/graph-image-generator"
}
```

### ```/image```

#### Supported methods 
* **POST**

#### Description
Generates PNG image from CX JSON.  You can simply _POST_ complete CX data as the body of request.

#### Sample Client Code
**Curl**

```
curl -X POST -v -H "content-type:application/json" --data-binary "@network1.cx" http://192.168.99.100:5000/image > network1.png
```

This command generates an image of _network1.cx_ and save as _network1.png_ in your current directory.


### ```/image/:format```

#### Supported methods 
* **POST**

#### Description
Generates an image from a CX JSON.  You can specify image file format in the path parameter ___:format___.

Supported image formats are:

* png
* svg
* pdf

#### Sample Client Code
**Curl**

```
curl -X POST -v -H "content-type:application/json" --data-binary "@network1.cx" http://192.168.99.100:5000/image/svg > network1.svg
```

### ```/image/graphviz/:format```

#### Supported methods 
* **POST**

#### Description
Generates an image from a CX JSON using [graphviz](http://www.graphviz.org/) as rendering engine.  You can specify image file format in the path parameter ___:format___.

Supported image formats are:

* png
* svg
* pdf

#### Sample Client Code
**Curl**

```
curl -X POST -v -H "content-type:application/json" --data-binary "@network1.cx" http://192.168.99.100:5000/image/graphviz/svg > network1.svg
```
