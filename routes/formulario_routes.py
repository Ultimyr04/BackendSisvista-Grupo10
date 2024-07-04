from flask import Blueprint, request, jsonify
from schemas.preguntas_schema import  pregunta_schema, preguntas_schema
from schemas.respuestas_schema import respuesta_schema, respuestas_schema
from models.respuestas import Respuesta
from models.preguntas import Pregunta

formulario = Blueprint("formulario", __name__)

@formulario.route('/api/formulario/preguntas', methods=['GET'])
def get_preguntas():
    idtipotest = request.args.get('idtipotest', type= int)
    if not idtipotest:
        return jsonify({"error": "idtipotest es requerido"}),400
    
    preguntas = Pregunta.query.filter_by(idtipotest=idtipotest).all()
    result = preguntas_schema.dump(preguntas)
    return jsonify(result)


@formulario.route('/api/formulario/respuestas', methods=['GET'])
def get_respuestas():
    idtipotest = request.args.get('idtipotest', type=int)
    if not idtipotest:
        return jsonify({"error": "idtipotest es requerido"}), 400
    
    respuestas = Respuesta.query.filter_by(idtipotest=idtipotest).all()
    result = respuestas_schema.dump(respuestas)
    return jsonify(result)  
