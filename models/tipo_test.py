from utils.db import db

class TipoTest(db.Model):
    __tablename__ = 'tipotest'
    idtipotest = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def __init__ (self, nombre):
        self.nombre=nombre