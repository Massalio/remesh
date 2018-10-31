import os.path
import datetime

from flask import Flask, Blueprint, jsonify, request
from flask_restful import Api
from flask_cors import CORS

from config.app_config import APP_NAME
from config.app_config import APP_PREFIX
from config.mongodb import MONGO_DB_NAME
from config.logger import configure_logger

from resources.meters_resource import MetersResource, MeterResourceData
from resources.meter_switches_resource import MeterSwitchesResource, MeterSwitchesListResource

app = Flask(APP_NAME)
app.config['PROPAGATE_EXCEPTIONS'] = True
CORS(app)
api_bp = Blueprint('api', APP_NAME)
api = Api(api_bp, prefix=APP_PREFIX)

# connect to another MongoDB database
app.config['MONGO_DBNAME'] = MONGO_DB_NAME

configure_logger(app)

api.add_resource(MetersResource, '/meters')
api.add_resource(MeterResourceData, '/meters/meterConsumption')
api.add_resource(MeterSwitchesResource, '/meter_switches')
api.add_resource(MeterSwitchesListResource, '/meter_switches/list')

app.register_blueprint(api_bp)

@app.route('/')
def hello_world():
    return "REMESH online"


if __name__ == '__main__':
    app.logger.info("Starting Python Server Services...")
    app.run(host='rocky-headland-53719.herokuapp.com')
    app.logger.info("Started")
