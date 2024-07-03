from utils.db import db

class TestRespuesta(db.Model):
    __tablename__ = 'testrespuesta'
    idtestrespuesta = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'))
    idtipotest = db.Column(db.Integer, db.ForeignKey('tipotest.idtipotest'))
    pregunta = db.Column(db.Integer)
    respuesta = db.Column(db.Integer)


    def __init__(self, idusuario, idtipotest, pregunta, respuesta):
        self.idusuario = idusuario
        self.idtipotest = idtipotest
        self.pregunta = pregunta
        self.respuesta = respuesta
