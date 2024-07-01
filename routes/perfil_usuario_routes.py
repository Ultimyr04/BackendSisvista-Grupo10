from flask import Blueprint, request, jsonify, make_response
from models.perfil_usuario import PerfilUsuario
from models.user import Usuario
from models.test_respuesta import TestRespuesta
from models.test_puntaje import TestPuntaje
from models.nivel_ansiedad import NivelAnsiedad
from utils.db import db
from schemas.perfil_usuario_schema import perfil_usuario_schema

perfil_usuario_routes = Blueprint("perfil_usuario_routes", __name__)

@perfil_usuario_routes.route('/api/perfil_usuario_routes/perfil-usuario', methods=['POST'])
#@perfil_usuario_routes.route('/perfil-usuario', methods=['POST'])
def create_perfil_usuario():
    idusuario = request.json.get('idusuario')

    # Obtener idusuario correspondiente al id_usuario desde la tabla Usuario
    usuario = Usuario.query.filter_by(idusuario=idusuario).first()
    if not usuario:
        data = {
            'message': 'Usuario no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    # Crear nuevo perfil_usuario
    nuevo_perfil_usuario = PerfilUsuario(idusuario=idusuario)
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

#@perfil_usuario_routes.route('/api/perfil_usuario_routes/perfil-usuario/<int:id>', methods=['GET'])
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
