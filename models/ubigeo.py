from datetime import date
from utils.db import db


class Ubigeo(db.Model):
    __tablename__ = 'ubigeo'
    idubigeo = db.Column(db.Integer, primary_key=True)
    distrito = db.Column(db.String(50))
    provincia = db.Column(db.String(50))
    departamento = db.Column(db.String(50))
    poblacion = db.Column(db.Integer)
    superficie = db.Column(db.Numeric(10, 4))
    y = db.Column(db.Numeric(10, 4))
    x = db.Column(db.Numeric(10, 4))