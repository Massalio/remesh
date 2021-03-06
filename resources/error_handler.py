from flask import jsonify, make_response


class ErrorHandler:

    def __init__(self):
        pass

    @staticmethod
    def create_error_response(status_code, message):
        return make_response(
            jsonify(
                {
                    "status_code": status_code,
                    "message": message
                }
            ),
            status_code
        )
