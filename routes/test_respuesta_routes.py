from flask import Blueprint, request, jsonify, make_response
from models.test_respuesta import TestRespuesta
from models.test_puntaje import TestPuntaje
from models.nivel_ansiedad import NivelAnsiedad
from models.nivel_gad import NivelGad
from models.nivel_hama import NivelHama
from utils.db import db
from schemas.test_respuesta_schema import test_respuesta_schema, tests_respuesta_schema
from schemas.test_puntaje_schema import test_puntaje_schema
import logging

# Configuración de logging
logging.basicConfig(level=logging.DEBUG)

test_routes = Blueprint("test_routes", __name__)

@test_routes.route('/api/test_respuesta_routes/test', methods=['POST'])
def create_test():
    try:
        data = request.json
        logging.debug(f"Request data: {data}")
        
        idusuario = data.get('idusuario')
        respuestas = data.get('respuestas')
        idtipotest = data.get('idtipotest')
        
        logging.debug(f"Received idusuario: {idusuario}")
        logging.debug(f"Received respuestas: {respuestas}")
        logging.debug(f"Received idtipotest: {idtipotest}")

        if not idusuario or not respuestas or not idtipotest:
            return jsonify({"error": "Faltan datos necesarios."}), 400
        
        for respuesta in respuestas:
            pregunta_numero = respuesta.get('pregunta') 
            respuesta_valor = respuesta.get('respuesta') 

            if pregunta_numero is None or respuesta_valor is None:
                return jsonify({"error" : "Formato de respuesta incorrecto."}), 400
            
            nueva_respuesta = TestRespuesta(
                idtipotest=idtipotest,
                idusuario=idusuario,
                pregunta=pregunta_numero,
                respuesta=respuesta_valor
            )
            db.session.add(nueva_respuesta)
        
        db.session.commit()
        
        return jsonify({"message": "Respuestas guardadas correctamente."}), 201
    
    except SQLAlchemyError as e:
        db.session.rollback()
        logging.error(f"Error while processing the request: {str(e)}")
        return jsonify({"error": str(e)}), 500

    except Exception as e:
        logging.error(f"Exception details: {str(e)}")
        return jsonify({"error": str(e)}), 500


@test_routes.route('/api/test_respuesta_routes/test/suma_puntajes/<int:idusuario>', methods=['GET'])
def get_suma_puntajes(idusuario):
    """
    Endpoint para obtener la suma de puntajes de tests para un usuario específico.

    Se espera recibir:
    - idusuario: ID del usuario.

    Funcionamiento:
    - Filtra las respuestas de tests por ID de usuario.
    - Calcula la suma total de puntajes.

    Respuestas:
    - Retorna un JSON con la suma de puntajes y estado 200 si se encuentra el usuario y hay puntajes calculados.
    """
    # Filtrar registros por idusuario
    test_respuestas = TestRespuesta.query.filter_by(idusuario=idusuario).all()

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
    """
    Endpoint para obtener todas las respuestas de tests.

    Funcionamiento:
    - Obtiene todas las respuestas de tests almacenadas en la base de datos.

    Respuestas:
    - Retorna un JSON con todas las respuestas de tests y estado 200.
    """
    all_tests = TestRespuesta.query.all()
    result = tests_respuesta_schema.dump(all_tests)

    data = {
        'message': 'Todas las respuestas de los tests',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)
