from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import signal

app = Flask(__name__)
api = Api(app)

class ArduinoData(Resource):
    def get(self):
        # TODO: Implement actual calculations.
        data = {
            'high': 1,
            'moderate': 0,
            'low': 0
        }
        data['total'] = data['high'] + data ['moderate'] + data ['low']
        return data
# Return 200 with no data.
class HealthCheck (Resource):
    def get(self):
        return Response(status=200)

api.add_resource(ArduinoData, "/data")
api.add_resource(HealthCheck, "/ping")
