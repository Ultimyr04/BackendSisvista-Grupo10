from utils.db import db

class Respuesta(db.Model):
    __tablename__ = 'respuestas'

    idrespuesta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipotest = db.Column(db.Integer)
    textorespuesta = db.Column(db.String(100))

    def __init__(self, idtipotest, textorespuesta):
        self.idtipotest = idtipotest
        self.textorespuesta = textorespuesta
