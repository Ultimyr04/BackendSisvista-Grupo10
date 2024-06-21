from flask import Blueprint, request, jsonify, make_response
from models.test_puntaje import TestPuntaje
from models.test_respuesta import TestRespuesta
from models.nivel_ansiedad import NivelAnsiedad
from utils.db import db
from sqlalchemy.sql import func

test_puntaje_routes = Blueprint("test_puntaje_routes", __name__)

@test_puntaje_routes.route('/api/test_puntaje', methods=['POST'])
def create_test_puntaje():
    idusuario = request.json.get('idusuario')

    # Calcular la suma de los puntajes desde TestRespuesta
    suma_puntajes = db.session.query(func.sum(TestRespuesta.respuesta)).filter_by(idperfil=idusuario).scalar()

    if suma_puntajes is None:
        return make_response(jsonify({'message': 'No se encontraron respuestas para el usuario', 'status': 404}), 404)

    # Determinar el nivel de ansiedad
    nivel_ansiedad = NivelAnsiedad.query.filter(NivelAnsiedad.minrespuesta <= suma_puntajes, NivelAnsiedad.maxrespuesta >= suma_puntajes).first()

    if not nivel_ansiedad:
        return make_response(jsonify({'message': 'No se pudo determinar el nivel de ansiedad', 'status': 400}), 400)

    new_puntaje = TestPuntaje(totaltest1=suma_puntajes, totaltest2=0, totaltest3=0, idnivelansiedad=nivel_ansiedad.idnivelansiedad)
    db.session.add(new_puntaje)
    db.session.commit()

    data = {
        'message': 'Puntaje del test creado!',
        'status': 201
    }

    return make_response(jsonify(data), 201)

@test_puntaje_routes.route('/api/test_puntaje', methods=['GET'])
def get_tests_puntaje():
    all_tests_puntaje = TestPuntaje.query.all()
    result = tests_puntaje_schema.dump(all_tests_puntaje)

    data = {
        'message': 'Todos los puntajes de los tests',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

@test_puntaje_routes.route('/api/test_puntaje/<int:id>', methods=['GET'])
def get_test_puntaje(id):
    test_puntaje = TestPuntaje.query.get(id)

    if not test_puntaje:
        data = {
            'message': 'Puntaje no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    result = test_puntaje_schema.dump(test_puntaje)

    data = {
        'message': 'Puntaje encontrado',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

@test_puntaje_routes.route('/api/test_puntaje/<int:id>', methods=['PUT'])
def update_test_puntaje(id):
    test_puntaje = TestPuntaje.query.get(id)

    if not test_puntaje:
        data = {
            'message': 'Puntaje no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    totaltest1 = request.json.get('totaltest1')
    totaltest2 = request.json.get('totaltest2')
    totaltest3 = request.json.get('totaltest3')
    idnivelansiedad = request.json.get('idnivelansiedad')

    test_puntaje.totaltest1 = totaltest1
    test_puntaje.totaltest2 = totaltest2
    test_puntaje.totaltest3 = totaltest3
    test_puntaje.idnivelansiedad = idnivelansiedad
    
    db.session.commit()

    result = test_puntaje_schema.dump(test_puntaje)

    data = {
        'message': 'Puntaje actualizado',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

@test_puntaje_routes.route('/api/test_puntaje/<int:id>', methods=['DELETE'])
def delete_test_puntaje(id):
    test_puntaje = TestPuntaje.query.get(id)

    if not test_puntaje:
        data = {
            'message': 'Puntaje no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(test_puntaje)
    db.session.commit()

    data = {
        'message': 'Puntaje eliminado',
        'status': 200
    }

    return make_response(jsonify(data), 200)
