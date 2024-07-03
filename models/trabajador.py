from utils.db import db

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    idtrabajador = db.Column(db.Integer, primary_key=True)
    idpersona = db.Column(db.Integer, db.ForeignKey('persona.idpersona'))
    salario = db.Column(db.Numeric(6, 2))
    persona = db.relationship('Persona')
