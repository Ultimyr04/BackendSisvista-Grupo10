from utils.db import db

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    idestudiante = db.Column(db.Integer, primary_key=True)
    idpersona = db.Column(db.Integer, db.ForeignKey('persona.idpersona'))
    codigoalumno = db.Column(db.Integer)
    carrera = db.Column(db.String(50))
    persona = db.relationship('Persona')