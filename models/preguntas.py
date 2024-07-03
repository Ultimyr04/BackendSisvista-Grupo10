from utils.db import db

class Pregunta(db.Model):
    __tablename__ = 'preguntas'

    idpregunta = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idtipotest = db.Column(db.Integer)
    textopregunta = db.Column(db.String(200))

    def __init__(self, idtipotest, textopregunta):
        self.idtipotest = idtipotest
        self.textopregunta = textopregunta
