import json

from flask import request, jsonify, make_response, current_app
from flask_restful import Resource

from resources.error_handler import ErrorHandler

from model.meter import Meter

class MetersResource(Resource):

    def post(self):
        try:
            current_app.logger.info("Received MetersResource POST Request")
            meterData = json.loads(request.data)

            createMeterResponse = Meter.create(meterData["ID"], meterData["value"])

            current_app.logger.debug("Python Server Response: 200 - %s", createMeterResponse)
            return make_response(jsonify(createMeterResponse), 200)
        except ValueError:
            error = "Unable to handle MetersResource POST Request"
            current_app.logger.error("Python Server Response: 500 - %s", error)
            return ErrorHandler.create_error_response(500, error)




