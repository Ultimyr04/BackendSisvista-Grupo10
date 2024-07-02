from utils.db import db

class PerfilUsuario(db.Model):
    __tablename__ = 'perfilusuario'
    idperfil = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    imagenperfil = db.Column(db.VARCHAR(150), nullable=True)
    observaciones = db.Column(db.VARCHAR(255), nullable=True)

    def __init__(self, idusuario, imagenperfil=None, observaciones=None):
        self.idusuario = idusuario
        self.imagenperfil = imagenperfil
        self.observaciones = observaciones
