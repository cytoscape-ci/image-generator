from flask import Flask
from flask_restful import Resource, Api

from image_generator import ImageGenerator
from status import Status


app = Flask(__name__)
api = Api(app)

# Routing
api.add_resource(Status, '/')

api.add_resource(ImageGenerator, '/image')
# api.add_resource(ImageGenerator, '/image.pdf')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
