from flask_restful import Resource

from flask import send_file
from flask import request

import json
import logging

from graph.cx_reader import GraphGenerator as gg


class GraphvizImageGenerator(Resource):

    def post(self, img_type):
        logging.warn("--------type is " + img_type)

        data = request.stream.read()
        g = gg.get_graph(json.loads(data))
        file_name = gg.get_image(g, img_type=img_type, renderer='graphviz')
        return send_file(file_name, mimetype='image/' + img_type)

