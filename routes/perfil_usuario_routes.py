from flask import Blueprint, request, jsonify, make_response
from models.perfil_usuario import PerfilUsuario
from models.usuario import Usuario
from models.test_respuesta import TestRespuesta
from models.test_puntaje import TestPuntaje
from models.nivel_ansiedad import NivelAnsiedad
from utils.db import db
from schemas.perfil_usuario_schema import perfil_usuario_schema, perfiles_usuario_schema

perfil_usuario_routes = Blueprint("perfil_usuario_routes", __name__)

@perfil_usuario_routes.route('/api/perfil_usuario_routes/perfil-usuario', methods=['POST'])
def create_perfil_usuario():
    id_usuario = request.json.get('id_usuario')

    # Obtener idusuario correspondiente al id_usuario desde la tabla Usuario
    usuario = Usuario.query.filter_by(id_usuario=id_usuario).first()
    if not usuario:
        data = {
            'message': 'Usuario no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    idperfil = usuario.id_usuario  # Suponiendo que idperfil es el mismo que id_usuario

    # Obtener idpuntajes sumando respuestas correspondientes al idusuario en TestRespuesta
    sum_puntajes = db.session.query(db.func.sum(TestRespuesta.respuesta))\
                             .filter(TestRespuesta.idperfil == idperfil).scalar()

    # Obtener idpuntajes correspondiente al sum_puntajes desde la tabla TestPuntaje
    test_puntaje = TestPuntaje.query.filter(TestPuntaje.totaltest1 == sum_puntajes).first()
    if not test_puntaje:
        data = {
            'message': 'Puntaje no encontrado para el usuario',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    idpuntajes = test_puntaje.idpuntajes

    # Obtener idnivelansiedad basado en el rango de sum_puntajes en NivelAnsiedad
    nivel_ansiedad = NivelAnsiedad.query.filter(
        (NivelAnsiedad.minrespuesta <= sum_puntajes) &
        (NivelAnsiedad.maxrespuesta >= sum_puntajes)
    ).first()
    if not nivel_ansiedad:
        data = {
            'message': 'Nivel de ansiedad no encontrado para el puntaje',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    idnivelansiedad = nivel_ansiedad.idnivelansiedad

    # Crear nuevo perfil_usuario
    nuevo_perfil_usuario = PerfilUsuario(idusuario=id_usuario, idpuntajes=idpuntajes)
    db.session.add(nuevo_perfil_usuario)
    db.session.commit()

    # Serializar el objeto PerfilUsuario creado utilizando el esquema
    perfil_serializado = perfil_usuario_schema.dump(nuevo_perfil_usuario)

    data = {
        'message': 'Perfil de usuario creado exitosamente',
        'status': 201,
        'data': perfil_serializado
    }

    return make_response(jsonify(data), 201)

@perfil_usuario_routes.route('/api/perfil_usuario_routes/perfil-usuario/<int:id>', methods=['GET'])
def get_perfil_usuario(id):
    perfil_usuario = PerfilUsuario.query.get(id)

    if not perfil_usuario:
        data = {
            'message': 'Perfil de usuario no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    # Serializar el objeto PerfilUsuario encontrado utilizando el esquema
    perfil_serializado = perfil_usuario_schema.dump(perfil_usuario)

    data = {
        'message': 'Perfil de usuario encontrado',
        'status': 200,
        'data': perfil_serializado
    }

    return make_response(jsonify(data), 200)

# Agregar más rutas según sea necesario (actualización, eliminación, etc.)
