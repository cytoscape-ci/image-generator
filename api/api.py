from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class ImageGeneratorApi(Resource):

    def get(self):
        status = {
            'serviceName': 'Graph image generator',
            'version': 'v1'
        }
        return status


api.add_resource(ImageGeneratorApi, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
