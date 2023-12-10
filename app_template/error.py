
from flask import jsonify, request, current_app
# from . import app

class InvalidAPIUsage(Exception):
    status_code =  400

    def __init__(self, message, status_code=status_code, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
        current_app.logger.info(f"{status_code}\t{message}", extra=payload)
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv["message"] = self.message
        return rv


