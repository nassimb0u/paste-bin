from . import db
from sqlalchemy import Text
from marshmallow import Schema, fields as FM
from config import ID_CONFIG


class Paste(db.Model):
    id = db.Column(db.String(ID_CONFIG['size']*2), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.Text, nullable=False)

    def __init__(self, id, title, body):
        self.id = id
        self.title = title
        self.body = body

    def insert(self):
        db.session.add(self)
        db.session.commit()

class PasteSchema(Schema):
    id = FM.Str()
    title = FM.Str()
    body = FM.Str()
