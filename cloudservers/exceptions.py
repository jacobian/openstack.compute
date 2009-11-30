class CloudServersException(Exception):
    def __init__(self, code, message=None, details=None):
        self.code = code
        self.message = message or self.__class__.message
        self.details = details
        
    def __str__(self):
        return "%s (HTTP %s)" % (self.message, self.code)

class BadRequest(CloudServersException):
    http_status = 400
    message = "Bad request"

class Unauthorized(CloudServersException):
    http_status = 401
    message = "Unauthorized"

class Forbidden(CloudServersException):
    http_status = 403
    message = "Forbidden"
    
class NotFound(CloudServersException):
    http_status = 404
    message = "Not found"

class OverLimit(CloudServersException):
    http_status = 413
    message = "Over limit"

_code_map = dict((c.http_status, c) for c in CloudServersException.__subclasses__())

def from_response(response, body):
    """
    Return an instance of a CloudServersException or subclass
    based on an httplib2 response. 
    
    Usage::
    
        resp, body = http.request(...)
        if resp.status != 200:
            raise exception_from_response(resp, body)
    """
    cls = _code_map.get(response.status, CloudServersException)
    if body:
        return cls(**body['cloudServersFault'])
    else:
        return cls(code=response.status)