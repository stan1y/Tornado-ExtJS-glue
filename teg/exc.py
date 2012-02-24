import json
import logging
import tornado.web

log = logging.getLogger(__name__)

class TegException(tornado.web.HTTPError):
    def __init__(self, status_code=None, msg=None, *args):
        if status_code == None:
            self.status_code = self.http_status()
        else:
            self.status_code = status_code
        self.log_message = msg
        self.args = args
        self.data_map = {
            'error': self.__class__.__name__
        }

    def data(self):
        return self.data_map

    def json(self):
        return json.dumps(self.data())

    def http_status(self):
        return 500

    def append(self, key, value):
        self.data_map[key] = value
        
class BadArguments(TegException):
    def http_status(self):
        return 400
        
    def reason(self, msg):
        self.append('reason', msg)
        return self
        
class Unauthorized(TegException):
    def http_status(self):
        return 401
        
class AccessDenied(TegException):
    def http_status(self):
        return 403
        
class NotFound(TegException):
    def http_status(self):
        return 404
    
    def object_id(self, oid):
        self.append('object_id', oid)
        return self