from flask import Blueprint, request, jsonify, make_response
from models.test_puntaje import TestPuntaje
from models.test_respuesta import TestRespuesta
from models.nivel_ansiedad import NivelAnsiedad
from schemas.test_puntaje_schema import tests_puntaje_schema, test_puntaje_schema
from utils.db import db
from sqlalchemy.sql import func

test_puntaje_routes = Blueprint("test_puntaje_routes", __name__)

@test_puntaje_routes.route('/api/test_puntaje', methods=['POST'])
def create_test_puntaje():
    """
    Endpoint para crear el puntaje de un test.

    Se espera recibir:
    - idusuario: ID del usuario que realiza el test.
    - idtipotest: Tipo de test (1 para test1, 2 para test2, 3 para test3).
    - promedio: Promedio de puntajes obtenido en el test.

    Funcionamiento:
    - Calcula la suma de los puntajes desde TestRespuesta.
    - Calcula el promedio de los puntajes (totaltest1 + totaltest2 + totaltest3).
    - Determina el nivel de ansiedad basado en el promedio de puntajes.
    - Guarda el puntaje del test en la tabla TestPuntaje.

    Respuestas:
    - Retorna un JSON con mensaje de éxito, estado 201 y los datos del puntaje creado.
    """
    idusuario = request.json.get('idusuario')
    idtipotest = request.json.get('idtipotest')
    idperfil = request.json.get('idperfil')

    # Calcular la suma de los puntajes desde TestRespuesta
    suma_puntajes = db.session.query(func.sum(TestRespuesta.respuesta)).filter_by(idusuario=idusuario, idtipotest=idtipotest).scalar()

    if suma_puntajes is None:
        return make_response(jsonify({'message': 'No se encontraron respuestas para el usuario', 'status': 404}), 404)

    # Calcular el promedio de los puntajes
    promedio = (suma_puntajes * 1.0) / 3.0  # Calculamos el promedio

    # Determinar el nivel de ansiedad
    nivel_ansiedad = NivelAnsiedad.query.filter(NivelAnsiedad.minpromedio <= promedio, NivelAnsiedad.maxpromedio >= promedio).first()

    if not nivel_ansiedad:
        return make_response(jsonify({'message': 'No se pudo determinar el nivel de ansiedad', 'status': 400}), 400)

    new_puntaje = TestPuntaje(
        totaltest1=suma_puntajes if idtipotest == 1 else 0,
        totaltest2=suma_puntajes if idtipotest == 2 else 0,
        totaltest3=suma_puntajes if idtipotest == 3 else 0,
        promedio=promedio,
        idnivelansiedad=nivel_ansiedad.idnivelansiedad,
        idperfil=idperfil
    )
    db.session.add(new_puntaje)
    db.session.commit()

    data = {
        'message': 'Puntaje del test creado!',
        'status': 201,
        'data': test_puntaje_schema.dump(new_puntaje)
    }

    return make_response(jsonify(data), 201)


@test_puntaje_routes.route('/api/test_puntaje', methods=['GET'])
def get_tests_puntajes():
    """
    Endpoint para obtener todos los puntajes de tests.

    Funcionamiento:
    - Obtiene todos los puntajes de tests almacenados en la base de datos.

    Respuestas:
    - Retorna un JSON con todos los puntajes de tests y estado 200.
    """
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
    """
    Endpoint para obtener un puntaje de test específico por su ID.

    Se espera recibir:
    - id: ID del puntaje de test.

    Funcionamiento:
    - Busca el puntaje de test por su ID.
    - Si no se encuentra, retorna un mensaje de error.
    - Si se encuentra, retorna los datos del puntaje de test.

    Respuestas:
    - Retorna un JSON con los datos del puntaje de test y estado 200 si se encuentra.
    - Retorna un mensaje de error y estado 404 si no se encuentra.
    """
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
    """
    Endpoint para actualizar un puntaje de test específico por su ID.

    Se espera recibir:
    - id: ID del puntaje de test.

    Funcionamiento:
    - Busca el puntaje de test por su ID.
    - Si no se encuentra, retorna un mensaje de error.
    - Si se encuentra, actualiza los datos del puntaje de test y guarda los cambios.
    - Retorna los datos actualizados del puntaje de test.

    Respuestas:
    - Retorna un JSON con los datos actualizados del puntaje de test y estado 200 si se actualiza.
    - Retorna un mensaje de error y estado 404 si no se encuentra.
    """
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
    promedio = request.json.get('promedio')
    idnivelansiedad = request.json.get('idnivelansiedad')
    idperfil = request.json.get('idperfil')

    test_puntaje.totaltest1 = totaltest1 if totaltest1 is not None else test_puntaje.totaltest1
    test_puntaje.totaltest2 = totaltest2 if totaltest2 is not None else test_puntaje.totaltest2
    test_puntaje.totaltest3 = totaltest3 if totaltest3 is not None else test_puntaje.totaltest3
    test_puntaje.promedio = promedio if promedio is not None else test_puntaje.promedio
    test_puntaje.idnivelansiedad = idnivelansiedad if idnivelansiedad is not None else test_puntaje.idnivelansiedad
    test_puntaje.idperfil = idperfil if idperfil is not None else test_puntaje.idperfil

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
    """
    Endpoint para eliminar un puntaje de test específico por su ID.

    Se espera recibir:
    - id: ID del puntaje de test.

    Funcionamiento:
    - Busca el puntaje de test por su ID.
    - Si no se encuentra, retorna un mensaje de error.
    - Si se encuentra, elimina el puntaje de test de la base de datos.
    - Retorna un mensaje de éxito.

    Respuestas:
    - Retorna un mensaje de éxito y estado 200 si se elimina el puntaje de test.
    - Retorna un mensaje de error y estado 404 si no se encuentra.
    """
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

