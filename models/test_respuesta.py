from utils.db import db

class TestRespuesta(db.Model):
    __tablename__ = 'testrespuesta'
    idtipotest = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'))
    pregunta = db.Column(db.Integer, primary_key=True)
    respuesta = db.Column(db.Integer)

    def __init__ (self, idtipotest, idusuario, pregunta, respuesta):
        self.idtipotest=idtipotest
        self.idusuario=idusuario
        self.pregunta=pregunta
        self.respuesta=respuesta