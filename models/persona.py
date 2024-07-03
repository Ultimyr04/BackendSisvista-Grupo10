from datetime import date
from utils.db import db
from models.ubigeo import Ubigeo

class Persona(db.Model):
    __tablename__ = 'persona'
    idpersona = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    idubigeo = db.Column(db.Integer, db.ForeignKey('ubigeo.idubigeo'))
    genero = db.Column(db.String(50))
    fechanacimiento = db.Column(db.Date)

    ubigeo = db.relationship('Ubigeo', backref = 'persona')
