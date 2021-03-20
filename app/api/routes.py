from . import api_blueprint
from flask import request
from flask_restx import Api, Resource, fields, marshal
from ..models import Paste, generate_id
from time import time
from config import ID_CONFIG
from .errors import not_found

api = Api(api_blueprint, title='Pastebin API', description='A pastebin like API',
validate=True)
name_space = api.namespace('pastes')

id_field = fields.String(required=True, description='ID of the paste',
example='f17eb084176d')

title_field = fields.String(required=True, description='Title of the paste',
max_length=100, example='Documentation')

body_field = fields.String(required=True, description='Body of the paste',
    example='This is the body of the paste')

paste_model = name_space.model('Paste', {
    'id': id_field
})

paste_detail_model = name_space.inherit('PasteDetail', paste_model, {
    'title': title_field,
    'body': body_field
})  

error_model = name_space.model('Error', {
    'errors': fields.Raw(required=True, description='Errors', 
    example={"title": "'title' is a required property"}),
    'message': fields.String(required=True,
    description='A human-readable message providing more details about the error',
    example='Input payload validation failed'),
})

post_paste_model = name_space.model('PostePaste', {
    'title': title_field,
    'body': body_field
})

@name_space.route('/')
class PasteList(Resource):
    @name_space.doc(body=post_paste_model)
    @name_space.response(400, 'Bad request', error_model)
    @name_space.response(200, 'Success', paste_model)
    def post(self):
        body = request.get_json()
        f = 1000
        if ID_CONFIG['time_unit'] == 'us':
            f *= 1000
        timestamp = round(time()*f)
        paste_id = generate_id(timestamp)
        title = body['title']
        body = body['body']
        paste = Paste(paste_id, title, body)
        paste.insert()
        return marshal(paste, paste_model)


@name_space.route('/<string:id>')
class PasteDetail(Resource):
    @name_space.response(404, 'Resource not found', error_model)
    @name_space.response(200, 'Success', paste_detail_model)
    def get(self, id):
        paste = Paste.query.get(id)
        if paste is None:
            return marshal(not_found, error_model, skip_none=True), 404
        return marshal(paste, paste_detail_model)
