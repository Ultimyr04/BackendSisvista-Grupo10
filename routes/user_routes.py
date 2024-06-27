from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import Usuario, Estudiante, Psicologo, Trabajador
from utils.db import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    
    if not usuario or not contrasena:
        return jsonify({"error": "Usuario y contraseña son requeridos"}), 400
    
    try:
        user = Usuario.query.filter_by(nickusuario=usuario).first()
        if user:
            print(f"Usuario encontrado: {user.nickusuario}")
            print(f"Contraseña almacenada: {user.contrasena}")
            print(f"Contraseña proporcionada: {contrasena}")
            if user.contrasena == contrasena:
                print("Contraseña correcta")
                # Verifica si el usuario es un estudiante
                estudiante = Estudiante.query.filter_by(idpersona=user.idpersona).first()
                if estudiante:
                    role = 'ESTUDIANTE'
                else:
                    # Verifica si el usuario es un psicólogo
                    psicologo = Psicologo.query.join(Trabajador, Psicologo.idtrabajador == Trabajador.idtrabajador).filter(Trabajador.idpersona == user.idpersona).first()
                    if psicologo:
                        role = 'PSICOLOGO'
                    else:
                        role = 'UNKNOWN'
                
                access_token = create_access_token(identity={"usuario": user.nickusuario, "rol": role})
                return jsonify(access_token=access_token), 200
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
