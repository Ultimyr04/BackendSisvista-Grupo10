from utils.db import db

class PerfilUsuario(db.Model):
    __tablename__ = 'perfilusuario'
    idperfil = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    imagenperfil = db.Column(db.VARCHAR(50))

    def __init__(self, idusuario, imagenperfil=None):
        self.idusuario = idusuario
        self.imagenperfil = None