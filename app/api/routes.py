from . import api
from flask import request
from flask_restplus import Api, Resource
from ..models import Paste, PasteSchema
from time import time
from random import randint, shuffle
from config import ID_CONFIG

api = Api(api, version='1.0', doc='/docs')
name_space = api.namespace('pastes', description='Pastebin API')

def generate_id(timestamp):
    uid = f'{timestamp:x}'
    print(timestamp, uid)
    bytes_list = []
    i = 0
    for _ in range(ID_CONFIG['size']):
        s = uid[i:i+2] + '0'*(2-len(uid[i:i+2]))
        bytes_list.append(s)
        i += 2
    shuffle(bytes_list)
    return ''.join(bytes_list)
    
    


@name_space.route("/")
class PasteList(Resource):
    def post(self):
        body = request.get_json()
        print(type(body))
        if body is None:
            name_space.abort(400)
        f = 1000
        if ID_CONFIG['time_unit'] == 'us':
            f *= 1000
        timestamp = round(time()*f)
        paste_id = generate_id(timestamp)
        paste = Paste(paste_id, body.get('title'), body.get('body'))
        paste.insert()
        return {
            "success": True,
            "created": paste_id
        }


@name_space.route("/<string:id>")
class PasteDetail(Resource):
    def get(self, id):
        paste = Paste.query.get(id)
        if paste is None:
            name_space.abort(404)
        schema = PasteSchema()
        return {
            "success": True,
            "paste": schema.dump(paste)
        }
