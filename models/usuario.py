from datetime import date
from utils.db import db
from models.persona import Persona
from models.perfil_usuario import PerfilUsuario

class Usuario(db.Model):
    __tablename__ = 'usuario'
    idusuario = db.Column(db.Integer, primary_key=True)
    idpersona = db.Column(db.Integer, db.ForeignKey('persona.idpersona'))
    email = db.Column(db.String(100), unique=True)
    telefono = db.Column(db.String(50), unique=True)
    nickusuario = db.Column(db.String(50), unique=True)
    contrasena = db.Column(db.String(255))
    fecharegistro = db.Column(db.Date, default=date.today)
    rol = db.Column(db.String(30))
    persona = db.relationship('Persona', backref ='usuario')
    perfil_usuario = db.relationship('PerfilUsuario', backref='usuario')

    def to_dict(self):
        return{
            'idusuario': self.idusuario,
            'usuario' : self.nickusuario,
            'rol': self.rol
        }


