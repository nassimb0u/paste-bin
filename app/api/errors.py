class ActionError(Exception):
    def __init__(self, error_type, status_code, message):
        self.error_type = error_type
        self.status_code = status_code
        self.message = message

class InvalidRequestError(ActionError):
    def __init__(self, message, param):
        super().__init__('invalid_request_error', 400, message)
        self.param = param

handle_bad_request_400 = {
    'success': False,
    'status': 400,
    'message': 'The browser (or proxy) sent a request that this server could \
not understand.'
}

handle_not_allowed_405 = {
    "success": False,
    "status": 405,
    "message": "The method is not allowed for the requested URL"
}

handle_not_found_404 = {
    'success': False,
    'status': 404,
    'message': 'Resource not found'
}
