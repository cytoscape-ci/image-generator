from flask import Flask
from flask_restful import Resource, Api

from bitmap_image_generator import BitmapImageGenerator
from vector_image_generator import VectorImageGenerator
from graphviz_image_generator import GraphvizImageGenerator

from status import Status


app = Flask(__name__)
api = Api(app)

# Routing
api.add_resource(Status, '/')

api.add_resource(GraphvizImageGenerator, '/image/graphviz/<string:img_type>')
api.add_resource(VectorImageGenerator, '/image/<string:img_type>')
api.add_resource(BitmapImageGenerator, '/image')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
