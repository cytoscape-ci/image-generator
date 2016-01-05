from flask_restful import Resource


class Status(Resource):

    def get(self):
        status = {
            'serviceName': 'Graph image generator',
            'version': 'v1'
        }
        return status
