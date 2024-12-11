# routes/estudiante_routes.py

from flask import Blueprint, request, jsonify
from models.estudiante import Estudiante
from models.persona import Persona
from utils.db import db

estudiante_routes = Blueprint("estudiante_routes", __name__)

@estudiante_routes.route('/api/estudiantes/buscar', methods=['GET'])
def buscar_estudiante():
    nombre = request.args.get('nombre', None)
    if nombre is None:
        return jsonify({"error": "Nombre de estudiante no proporcionado"}), 400
    
    # Buscar el estudiante por nombre a través de la relación con Persona
    estudiante = Estudiante.query.join(Estudiante.persona).filter(db.func.lower(db.func.concat(Persona.nombres, ' ', Persona.apellidos)).ilike(f"%{nombre.lower()}%")).first()
    
    if estudiante:
        return jsonify({"mensaje": "Estudiante encontrado", "estudiante": {"id": estudiante.idestudiante, "nombre": estudiante.persona.nombres}}), 200
    else:
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404
