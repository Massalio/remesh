import json

from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from resources.error_handler import ErrorHandler

from model.meter_switch import MeterSwitch

class MeterSwitchesResource(Resource):

    def post(self):
        try:
            current_app.logger.info("Received MeterSwitchesResource POST Request")
            meterSwitchData = json.loads(request.data)

            createMeterSwitchResponse = MeterSwitch.create(meterSwitchData["ID"], meterSwitchData["value"])

            current_app.logger.debug("Python Server Response: 200 - %s", createMeterSwitchResponse)
            return make_response(jsonify(createMeterSwitchResponse), 200)
        except ValueError:
            error = "Unable to handle MetersResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)

class MeterSwitchesListResource(Resource):

    def post(self):
        try:
            current_app.logger.info("Received MeterSwitchesListResource POST Request")
            meterSwitchData = json.loads(request.data)

            meterSwitchesResponse = MeterSwitch.get(meterSwitchData["listOfIDs"])

            current_app.logger.debug("Python Server Response: 200 - %s", meterSwitchesResponse)
            return make_response(jsonify(meterSwitchesResponse), 200)
        except ValueError:
            error = "Unable to handle CategoriesResource GET Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)
