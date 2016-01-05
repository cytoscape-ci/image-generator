from flask_restful import Resource
import graph_tool.all as gt

from flask import send_file
from flask import request

import logging
import json

from graph.cx_reader import GraphGenerator


class ImageGenerator(Resource):

    def __init__(self):
        self.__gg = GraphGenerator()

    def get(self):
        print("Generating graph...")

        g = gt.price_network(500)
        pos = gt.sfdp_layout(g)
        file_name = '/app/images/graph1.png'
        gt.graph_draw(g, pos=pos, output_size=(1000, 1000), output=file_name)

        return send_file(file_name, mimetype='image/png')

    def post(self):
        data = request.stream.read()

        g = self.__gg.getGraph(json.loads(data))

        logging.warning(g)

        file_name = self.__gg.getImage(g)
        return send_file(file_name, mimetype='image/png')
