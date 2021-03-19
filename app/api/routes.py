from . import api
from flask import request
from flask_restplus import Api, Resource
from ..models import Paste, PasteSchema, generate_id
from time import time
from config import ID_CONFIG

api = Api(api, title='Pastebin API', description='A pastebin like API', ordered=True)
name_space = api.namespace('pastes')

@name_space.route('/')
class PasteList(Resource):
    def post(self):
        body = request.get_json()
        print(type(body))
        if body is None:
            name_space.abort(400, **handle_bad_request_400)
        f = 1000
        if ID_CONFIG['time_unit'] == 'us':
            f *= 1000
        timestamp = round(time()*f)
        paste_id = generate_id(timestamp)
        try:
            title = body['title']
            body = body['body']
        except KeyError as e:
            raise InvalidRequestError('missing required argument', e.args[0])
        if type(title) != str:
            raise InvalidRequestError(
                'wrong parameter type, string expected',
                'title')
        if type(body) != str:
            raise InvalidRequestError(
                'wrong parameter type, string expected',
                'body')
        paste = Paste(paste_id, title, body)
        paste.insert()
        return {
            'success': True,
            'created': paste_id
        }


@name_space.route('/<string:id>')
class PasteDetail(Resource):
    def get(self, id):
        paste = Paste.query.get(id)
        if paste is None:
            name_space.abort(404, **handle_not_found_404)
        schema = PasteSchema()
        return {
            'success': True,
            'paste': schema.dump(paste)
        }


class ActionError(Exception):
    def __init__(self, error_type, status_code, message):
        self.error_type = error_type
        self.status_code = status_code
        self.message = message

class InvalidRequestError(ActionError):
    def __init__(self, message, param):
        super().__init__('invalid_request_error', 400, message)
        self.param = param


@name_space.errorhandler(InvalidRequestError)
def handle_InvalidRequestError(error):
    return {
        'success': False,
        'status': error.status_code,
        'type': error.error_type,
        'message': error.message,
        'param': error.param
    }, error.status_code

handle_bad_request_400 = {
    'success': False,
    'status': 400,
    'message': 'The browser (or proxy) sent a request that this server could \
not understand.'
}

handle_not_found_404 = {
    'success': False,
    'status': 404,
    'message': 'resource not found'
}
