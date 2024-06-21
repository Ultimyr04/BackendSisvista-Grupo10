from flask import Blueprint, request, jsonify, make_response
from models.test_respuesta import TestRespuesta
from models.test_puntaje import TestPuntaje
from utils.db import db
from schemas.test_respuesta_schema import test_respuesta_schema, tests_respuesta_schema
from schemas.test_puntaje_schema import test_puntaje_schema

test_routes = Blueprint("test_routes", __name__)

@test_routes.route('/api/test_respuesta_routes/test', methods=['POST'])
def create_test():
    idusuario = request.json.get('idusuario')
    respuestas = request.json.get('respuestas')  # Lista de diccionarios con 'pregunta' y 'respuesta'
    idtipotest = request.json.get('idtipotest')  # Tipo de test

    # Validar que se hayan proporcionado exactamente 10 respuestas
    if not respuestas or len(respuestas) != 10:
        return make_response(jsonify({'message': 'Debe proporcionar 10 respuestas', 'status': 400}), 400)

    idperfil = idusuario  # Asumiendo que idperfil es el mismo que idusuario
    total_puntaje = sum([item['respuesta'] for item in respuestas])

    # Guardar cada respuesta en la tabla TestRespuesta
    for item in respuestas:
        pregunta = item['pregunta']
        respuesta = item['respuesta']

        new_respuesta = TestRespuesta(idtipotest, idperfil, pregunta, respuesta)
        db.session.add(new_respuesta)

    # Guardar el puntaje total en la tabla TestPuntaje
    new_puntaje = TestPuntaje(totaltest1=total_puntaje, totaltest2=0, totaltest3=0, idnivelansiedad=None)
    db.session.add(new_puntaje)
    db.session.commit()

    data = {
        'message': 'Respuestas del test creadas!',
        'status': 201
    }

    return make_response(jsonify(data), 201)

@test_routes.route('/api/test_respuesta_routes/test/suma_puntajes/<int:idusuario>', methods=['GET'])
def get_suma_puntajes(idusuario):
    # Filtrar registros por idusuario
    test_respuestas = TestRespuesta.query.filter_by(idperfil=idusuario).all()

    if not test_respuestas:
        return make_response(jsonify({'message': 'No se encontraron registros para el usuario', 'status': 404}), 404)

    # Calcular la suma de los puntajes
    suma_puntajes = sum([respuesta.respuesta for respuesta in test_respuestas])

    data = {
        'message': 'Suma de puntajes calculada',
        'status': 200,
        'suma_puntajes': suma_puntajes
    }

    return make_response(jsonify(data), 200)

@test_routes.route('/api/test_respuesta_routes/test', methods=['GET'])
def get_tests():
    all_tests = TestRespuesta.query.all()
    result = tests_respuesta_schema.dump(all_tests)

    data = {
        'message': 'Todas las respuestas de los tests',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)