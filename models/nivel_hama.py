from utils.db import db

class NivelHama(db.Model):
    __tablename__ = 'nivelhama'
    idnivelansiedad = db.Column(db.Integer, primary_key=True)
    minrespuesta = db.Column(db.Integer)
    maxrespuesta = db.Column(db.Integer)
    nivel = db.Column(db.String(50))

    def __init__(self, minrespuesta, maxrespuesta, nivel):
        self.minrespuesta = minrespuesta
        self.maxrespuesta = maxrespuesta
        self.nivel = nivel
