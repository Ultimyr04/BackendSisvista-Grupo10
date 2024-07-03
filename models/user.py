from datetime import date
from utils.db import db

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
    persona = db.relationship('Persona')

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    idestudiante = db.Column(db.Integer, primary_key=True)
    idpersona = db.Column(db.Integer, db.ForeignKey('persona.idpersona'))
    codigoalumno = db.Column(db.Integer)
    carrera = db.Column(db.String(50))
    persona = db.relationship('Persona')

class Trabajador(db.Model):
    __tablename__ = 'trabajador'
    idtrabajador = db.Column(db.Integer, primary_key=True)
    idpersona = db.Column(db.Integer, db.ForeignKey('persona.idpersona'))
    salario = db.Column(db.Numeric(6, 2))
    persona = db.relationship('Persona')

class Psicologo(db.Model):
    __tablename__ = 'psicologo'
    idpsicologo = db.Column(db.Integer, primary_key=True)
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.idtrabajador'))
    especialidad = db.Column(db.String(50))
    trabajador = db.relationship('Trabajador')

class AdministradorSoftware(db.Model):
    __tablename__ = 'administradorsoftware'
    idadministrador = db.Column(db.Integer, primary_key=True)
    idtrabajador = db.Column(db.Integer, db.ForeignKey('trabajador.idtrabajador'))
    trabajador = db.relationship('Trabajador')
