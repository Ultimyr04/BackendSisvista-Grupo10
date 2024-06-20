from utils.db import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'usuario'
    idusuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(50), unique=True, nullable=True)
    genero = db.Column(db.String(50), nullable=False)
    fechanacimiento = db.Column(db.Date, nullable=True)
    nickusuario = db.Column(db.String(50), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(30), nullable=False)
    fecharegistro = db.Column(db.Date, nullable=False, default=db.func.current_date())

    def set_password(self, password):
        self.contrasena = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contrasena, password)
