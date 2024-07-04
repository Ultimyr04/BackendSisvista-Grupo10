from flask import Blueprint, request, jsonify
from models.usuario import Usuario 
from models.estudiante import Estudiante
from models.persona import Persona
from models.ubigeo import Ubigeo
from models.perfil_usuario import PerfilUsuario
from utils.db import db
from datetime import datetime

register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    print("DATA RECIBIDA: ",data) #Linea para depurar y ver errores
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    idubigeo = data.get('idubigeo')
    email = data.get('email')
    telefono = data.get('telefono')
    genero = data.get('genero')
    fechanacimiento = data.get('fechanacimiento')
    nickusuario = data.get('nickusuario')
    contrasena = data.get('contrasena')   
    
    if not (nombres and apellidos and idubigeo and email and telefono and genero and fechanacimiento and nickusuario and contrasena):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    try:
        # Verificar si el usuario, email o teléfono ya existen
        if Usuario.query.filter((Usuario.nickusuario == nickusuario) | (Usuario.email == email) | (Usuario.telefono == telefono)).first():
            return jsonify({"error": "El usuario, email o teléfono ya existen"}), 400

        #Convierte la fecha de nacimiento de formato de cadena a DATE
        fechanacimiento_DATE = datetime.strptime(fechanacimiento, '%Y-%m-%d').date()

        # Crear la nueva persona
        new_persona = Persona(
            nombres=nombres,
            apellidos=apellidos,
            idubigeo=int(idubigeo),
            genero=genero,
            fechanacimiento=fechanacimiento_DATE
        )
        db.session.add(new_persona)
        db.session.flush()  # Esto asegura que new_persona.idpersona esté disponible

        # Crear el nuevo usuario
        new_usuario = Usuario(
            idpersona=new_persona.idpersona,
            email=email,
            telefono=telefono,
            nickusuario=nickusuario,
            contrasena=contrasena,
            rol='ESTUDIANTE'
        )
        db.session.add(new_usuario)
        db.session.flush()  # Esto asegura que new_usuario.idusuario esté disponible

        # Crear el nuevo estudiante
        new_estudiante = Estudiante(
            idpersona=new_persona.idpersona
        )
        db.session.add(new_estudiante)
        db.session.commit()

        #Crear el nuevo perfilUsuario
        #Creandose con observaciones vacias (NONE)
        new_perfil_usuario = PerfilUsuario(
            idusuario=new_usuario.idusuario,
            observaciones= None
        )
        db.session.add(new_perfil_usuario)
        db.session.commit()

        return jsonify({"message": "Cuenta creada exitosamente"}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"error": "Error de integridad de datos: " + str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor: " + str(e)}), 500
