from flask_restful import Resource

from flask import send_file
from flask import request

import json

from graph.cx_reader import GraphGenerator as gg


class BitmapImageGenerator(Resource):

    def post(self):
        data = request.stream.read()
        g = gg.get_graph(json.loads(data))
        file_name = gg.get_image(g, 'png')
        return send_file(file_name, mimetype='image/png')
