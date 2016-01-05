import graph_tool.all as gt
from flask_restful import reqparse

import logging

import math


class GraphGenerator:

    def __init__(self):
        self.__parser = reqparse.RequestParser()

    def getGraph(self, cx_data):

        logging.warning(type(cx_data))

        g = gt.Graph()

        nodes = []
        edges = []

        for entry in cx_data:
            if 'nodes' in entry:
                for n in entry['nodes']:
                    nodes.append(n)
            elif 'edges' in entry:
                for e in entry['edges']:
                    edges.append(e)

        vmap = {}

        for node in nodes:
            v = g.add_vertex()
            node_id = node['@id']
            vmap[node_id] = v

        for edge in edges:
            source = vmap[edge['s']]
            target = vmap[edge['t']]
            e = g.add_edge(source, target)


        return g

    def getImage(self, g):
        pos = gt.sfdp_layout(g)

        node_color = g.new_vertex_property('vector<double>', val=[0, 0, 0, 0])
        node_fill_color = g.new_vertex_property('vector<double>', val=[0, 0.7, 0.8, 0.5])

        file_name = '/app/images/graph1.png'
        gt.graph_draw(g, pos=pos,
                      vertex_color=node_color,
                      vertex_fill_color=node_fill_color,
                      output_size=(1000, 1000), output=file_name)
        return file_name
