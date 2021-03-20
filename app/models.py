from . import db
from sqlalchemy import Text
from config import ID_CONFIG
from random import randint, shuffle


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
