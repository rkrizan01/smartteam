from database import Data
from flask import Flask, Response
from flask_restful import Resource, Api, reqparse
import json
import signal

app = Flask(__name__)
api = Api(app)

class ArduinoData(Resource):
    def get(self):
        return [d.__dict__ for d in Data.get_all()]

# Return 200 with no data.
class HealthCheck (Resource):
    def get(self):
        return Response(status=200)

api.add_resource(ArduinoData, "/data")
api.add_resource(HealthCheck, "/ping")
