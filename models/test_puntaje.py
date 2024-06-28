from utils.db import db

class TestPuntaje(db.Model):
    __tablename__ = 'testpuntaje'
    idpuntajes = db.Column(db.Integer, primary_key=True)
    totaltest1 = db.Column(db.Integer)
    totaltest2 = db.Column(db.Integer)
    totaltest3 = db.Column(db.Integer)
    idnivelansiedad = db.Column(db.Integer, db.ForeignKey('nivelansiedad.idnivelansiedad'))
    idperfil = db.Column(db.Integer, db.ForeignKey('perfilusuario.idperfil'))

    def __init__(self, totaltest1=None, totaltest2=None, totaltest3=None, idnivelansiedad=None, idperfil=None):
        self.totaltest1 = totaltest1
        self.totaltest2 = None
        self.totaltest3 = None
        self.idnivelansiedad = idnivelansiedad
        self.idperfil = idperfil