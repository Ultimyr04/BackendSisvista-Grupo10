from utils.db import db

class TestPuntaje(db.Model):
    __tablename__ = 'testpuntaje'
    idpuntajes = db.Column(db.Integer, primary_key=True)
    totaltest1 = db.Column(db.Integer)
    totaltest2 = db.Column(db.Integer)
    totaltest3 = db.Column(db.Integer)
    promedio = db.Column(db.Integer)
    idnivelansiedad = db.Column(db.Integer, db.ForeignKey('nivelansiedad.idnivelansiedad'))
    idperfil = db.Column(db.Integer, db.ForeignKey('perfilusuario.idperfil'))

    def __init__(self, totaltest1=None, totaltest2=None, totaltest3=None, promedio=None, idnivelansiedad=None, idperfil=None):
        self.totaltest1 = totaltest1
        self.totaltest2 = totaltest2
        self.totaltest3 = totaltest3
        self.promedio = promedio
        self.idnivelansiedad = idnivelansiedad
        self.idperfil = idperfil