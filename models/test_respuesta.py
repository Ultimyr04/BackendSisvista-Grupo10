from utils.db import db

class TestRespuesta(db.Model):
    __tablename__ = 'testrespuesta'
    idtipotest = db.Column(db.Integer)
    idperfil = db.Column(db.Integer, db.ForeignKey('perfilusuario.idperfil'))
    pregunta = db.Column(db.Integer)
    respuesta = db.Column(db.Integer)

    def __init__ (self, idtipotest, idperfil, pregunta, respuesta):
        self.idtipotest=idtipotest
        self.idperfil=idperfil
        self.pregunta=pregunta
        self.respuesta=respuesta