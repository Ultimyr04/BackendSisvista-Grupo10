from utils.db import db
from datetime import date

class NivelGad(db.Model):
    __tablename__ = 'citas'
    idcita = db.Column(db.Integer, primary_key=True)
    idpsicologo = db.Column(db.Integer, db.ForeignKey('psicologo.idpsicologo'))
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.idestudiante'))
    fecha = db.Column(db.Date, default=date.today)
    tipocita = db.Column(db.String(30))


    def __init__(self, idpsicologo, idestudiante, fecha, tipocita):
        self.idpsicologo = idpsicologo
        self.idestudiante = idestudiante
        self.fecha = fecha
        self.tipocita = tipocita