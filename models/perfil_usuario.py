from utils.db import db

class PerfilUsuario(db.Model):
    __tablename__ = 'perfilusuario'
    idperfil = db.Column(db.Integer, primary_key=True)
    idusuario = db.Column(db.Integer, db.ForeignKey('usuario.idusuario'), nullable=False)
    idpuntajes = db.Column(db.Integer, db.ForeignKey('test_puntaje.idpuntajes'))
    imagenperfil = db.Column(db.VARCHAR(50))

    def __init__(self, idusuario, imagenperfil=None, idpuntajes=None):
        self.idusuario = idusuario
        self.imagenperfil = None
        self.idpuntajes = idpuntajes