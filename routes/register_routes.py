from flask import Blueprint, request, jsonify
from models.user import Persona, Usuario, Estudiante, Ubigeo
from utils.db import db

register_user = Blueprint('register_user', __name__)

@register_user.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    nombres = data.get('nombres')
    apellidos = data.get('apellidos')
    idubigeo = data.get('idubigeo')
    email = data.get('email')
    telefono = data.get('telefono')
    genero = data.get('genero')
    nickusuario = data.get('nickusuario')
    contrasena = data.get('contrasena')
    
    if not (nombres and apellidos and idubigeo and email and telefono and genero and nickusuario and contrasena):
        return jsonify({"error": "Todos los campos son requeridos"}), 400

    try:
        # Verificar si el usuario o el email ya existen
        if Usuario.query.filter((Usuario.nickusuario == nickusuario) | (Usuario.email == email) | (Usuario.telefono == telefono)).first():
            return jsonify({"error": "El usuario, email o teléfono ya existen"}), 400

        # Crear la nueva persona
        new_persona = Persona(
            nombres=nombres,
            apellidos=apellidos,
            idubigeo=idubigeo,
            genero=genero
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
            idpersona=new_persona.idpersona,
            codigoalumno=None,  # Asigna el valor adecuado si está disponible
            carrera=None  # Asigna el valor adecuado si está disponible
        )
        db.session.add(new_estudiante)
        db.session.commit()

        return jsonify({"message": "Cuenta creada exitosamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
