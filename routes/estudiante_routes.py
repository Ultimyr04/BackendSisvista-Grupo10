# routes/estudiante_routes.py

from flask import Blueprint, request, jsonify
from models.estudiante import Estudiante
from utils.db import db

estudiante_routes = Blueprint("estudiante_routes", __name__)

@estudiante_routes.route('/api/estudiantes/buscar', methods=['GET'])
def buscar_estudiante():
    nombre = request.args.get('nombre', None)
    if nombre is None:
        return jsonify({"error": "Nombre de estudiante no proporcionado"}), 400
    
    estudiante = Estudiante.query.filter(Estudiante.nombre.ilike(f"%{nombre}%")).first()
    if estudiante:
        return jsonify({"mensaje": "Estudiante encontrado", "estudiante": {"id": estudiante.idestudiante, "nombre": estudiante.nombre}}), 200
    else:
        return jsonify({"mensaje": "Estudiante no encontrado"}), 404
