from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import Usuario, Estudiante, Psicologo, Trabajador
from models.persona import Persona
from utils.db import db

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/api/login', methods=['POST'])
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
            print(f"ID del Usuario: {user.idusuario}")  # Imprimir el ID del usuario
            if user.contrasena == contrasena:
                print("Contraseña correcta")

                # Obtener información de la persona
                persona = Persona.query.filter_by(idpersona=user.idpersona).first()
                if not persona:
                    return jsonify({"error": "No se encontró la persona asociada"}), 404

                print(f"Persona encontrada: {persona.nombres} {persona.apellidos}")

                # Verificar el rol del usuario
                estudiante = Estudiante.query.filter_by(idpersona=user.idpersona).first()
                if estudiante:
                    role = 'ESTUDIANTE'
                else:
                    psicologo = Psicologo.query.join(Trabajador, Psicologo.idtrabajador == Trabajador.idtrabajador).filter(Trabajador.idpersona == user.idpersona).first()
                    if psicologo:
                        role = 'PSICOLOGO'
                    else:
                        role = 'UNKNOWN'
                
                # Crear el token de acceso e incluir el idusuario en la carga útil
                #access_token = create_access_token(identity={"usuario": user.nickusuario, "idusuario": user.idusuario, "rol": role, "persona": {"nombres": persona.nombres, "apellidos": persona.apellidos}})

                response = {
                    "idusuario": user.idusuario,
                    "usuario": user.nickusuario,
                    "rol": role,
                    "persona":{
                        "nombres": persona.nombres,
                        "apellidos": persona.apellidos
                    }
                }

                return jsonify(response), 200
            else:
                print("Contraseña incorrecta")
        else:
            print("Usuario no encontrado")
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
