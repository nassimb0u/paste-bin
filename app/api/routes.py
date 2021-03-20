from . import api_blueprint
from flask import request
from flask_restplus import Api, Resource
from ..models import Paste, PasteSchema, generate_id
from time import time
from config import ID_CONFIG
from .errors import InvalidRequestError, handle_bad_request_400, handle_not_found_404

api = Api(api_blueprint, title='Pastebin API', description='A pastebin like API', ordered=True)
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


@api_blueprint.errorhandler(InvalidRequestError)
def handle_InvalidRequestError(error):
    return {
        'success': False,
        'status': error.status_code,
        'type': error.error_type,
        'message': error.message,
        'param': error.param
    }, error.status_code
