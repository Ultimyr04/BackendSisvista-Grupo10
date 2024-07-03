from utils.db import db

class Psicologo(db.Model):
    __tablename__ = 'psicologo'
    idpsicologo = db.Column(db.Integer, primary_key=True)
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.idtrabajador'))
    especialidad = db.Column(db.String(50))
    trabajador = db.relationship('Trabajador')
