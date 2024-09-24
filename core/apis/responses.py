from flask import Response, jsonify, make_response


class APIResponse(Response):
    @classmethod
    def respond(cls, data):
        return make_response(jsonify(data=data))
    
    @classmethod
    def error(cls, message, status_code=400):
        return make_response(jsonify(error=message), status_code)