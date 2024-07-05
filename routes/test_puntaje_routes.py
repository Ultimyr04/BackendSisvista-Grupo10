from flask import Blueprint, request, jsonify, make_response
from models.test_puntaje import TestPuntaje
from models.test_respuesta import TestRespuesta
from models.nivel_ansiedad import NivelAnsiedad
from models.perfil_usuario import PerfilUsuario
from schemas.test_puntaje_schema import tests_puntaje_schema, test_puntaje_schema
from utils.db import db
from sqlalchemy.sql import func
from models.usuario import Usuario
from models.persona import Persona

test_puntaje_routes = Blueprint("test_puntaje_routes", __name__)

@test_puntaje_routes.route('/api/test_puntaje', methods=['POST'])
def asignar_test_puntaje():
    data = request.get_json()
    idusuario = data['idusuario']
    idtipotest = data['idtipotest']

    #calcular la suma de respuestas con respecto a un usuario y test especifico
    total_score = db.session.query(func.sum(TestRespuesta.respuesta)).filter_by(idusuario=idusuario, idtipotest = idtipotest).scalar()

    #Buscar y actualizar TestPuntaje por tipotest
    testpuntaje = TestPuntaje.query.filter_by(idperfil = idusuario).first()  #Se asume que idusuario es igual al idperfil
    if testpuntaje:
        if idtipotest == 1:
            testpuntaje.totaltest1 = total_score
        elif idtipotest == 2:
            testpuntaje.totaltest2 = total_score
        elif idtipotest == 3:
            testpuntaje.totaltest3 = total_score

    
        if testpuntaje.totaltest1 is not None and testpuntaje.totaltest2 is not None and testpuntaje.totaltest3 is not None:
            testpuntaje.promedio = (testpuntaje.totaltest1 + testpuntaje.totaltest2 + testpuntaje.totaltest3) / 3

            nivelansiedad = NivelAnsiedad.query.filter(NivelAnsiedad.minrespuesta <= testpuntaje.promedio, NivelAnsiedad.maxrespuesta >= testpuntaje.promedio).first()
            if nivelansiedad:
                testpuntaje.idnivelansiedad = nivelansiedad.idnivelansiedad

        
        db.session.commit()
        return jsonify({"message": "Puntaje test actualizado correctamente"}), 200
    else:
        return jsonify({"error": "TestPuntaje no se actualizo correctamente"}), 404




   

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

    total_test1 = request.json.get('totaltest1')
    total_test2 = request.json.get('totaltest2')
    total_test3 = request.json.get('totaltest3')
    promedio = request.json.get('promedio')
    id_nivel_ansiedad = request.json.get('idnivelansiedad')
    id_perfil = request.json.get('idperfil')

    test_puntaje.totaltest1 = total_test1 if total_test1 is not None else test_puntaje.totaltest1
    test_puntaje.totaltest2 = total_test2 if total_test2 is not None else test_puntaje.totaltest2
    test_puntaje.totaltest3 = total_test3 if total_test3 is not None else test_puntaje.totaltest3
    test_puntaje.promedio = promedio if promedio is not None else test_puntaje.promedio
    test_puntaje.idnivelansiedad = id_nivel_ansiedad if id_nivel_ansiedad is not None else test_puntaje.idnivelansiedad
    test_puntaje.idperfil = id_perfil if id_perfil is not None else test_puntaje.idperfil

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


@test_puntaje_routes.route('/api/test_puntaje/details', methods=['GET'])
def get_test_puntaje_details():
    """
    Endpoint para obtener detalles de los puntajes de los tests incluyendo nombre, apellido y nivel de ansiedad.

    Respuestas:
    - Retorna un JSON con los detalles de los puntajes de los tests y estado 200.
    """
    # Realizar la consulta para unir las tablas necesarias
    results = db.session.query(
        TestPuntaje.totaltest1.label('Test1'),
        TestPuntaje.totaltest2.label('Test2'),
        TestPuntaje.totaltest3.label('Test3'),
        Persona.nombres.label('nombre'),
        Persona.apellidos.label('apellido'),
        NivelAnsiedad.nivel.label('nivel')
    ).join(
        PerfilUsuario, TestPuntaje.idperfil == PerfilUsuario.idperfil
    ).join(
        Usuario, PerfilUsuario.idusuario == Usuario.idusuario
    ).join(
        Persona, Usuario.idpersona == Persona.idpersona
    ).join(
        NivelAnsiedad, TestPuntaje.idnivelansiedad == NivelAnsiedad.idnivelansiedad
    ).all()

    # Preparar la respuesta
    data = [{
        'Test1': result.Test1,
        'Test2': result.Test2,
        'Test3': result.Test3,
        'nombre': result.nombre,
        'apellido': result.apellido,
        'nivel': result.nivel
    } for result in results]

    response = {
        'message': 'Detalle que muestra los puntajes de los tests',
        'status': 200,
        'data': data
    }

    return make_response(jsonify(response), 200)