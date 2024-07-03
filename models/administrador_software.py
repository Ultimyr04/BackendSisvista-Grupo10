from utils.db import db

class AdministradorSoftware(db.Model):
    __tablename__ = 'administradorsoftware'
    idadministrador = db.Column(db.Integer, primary_key=True)
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.idtrabajador'))
    trabajador = db.relationship('Trabajador')
