from flask import Blueprint, request, jsonify
from schemas.preguntas_schema import  pregunta_schema, preguntas_schema
from schemas.respuestas_schema import respuesta_schema, respuestas_schema
from models.respuestas import Respuesta
from models.preguntas import Pregunta

test_routes = Blueprint("test_routes", __name__)

@test_routes.route('/api/test_routes/preguntas', methods=['GET'])
def get_preguntas():
    idtipotest = request.args.get('idtipotest')
    preguntas = Pregunta.query.filter_by(idtipotest=idtipotest).all()
    result = preguntas_schema.dump(preguntas)
    return jsonify(result)

@test_routes.route('/api/test_routes/respuestas', methods=['GET'])
def get_respuestas():
    idtipotest = request.args.get('idtipotest')
    respuestas = Respuesta.query.filter_by(idtipotest=idtipotest).all()
    result = respuestas_schema.dump(respuestas)
    return jsonify(result)
