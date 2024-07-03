from flask import Blueprint, jsonify
from models.user import Usuario
from models.persona import Persona
from models.test_puntaje import TestPuntaje
from models.ubigeo import Ubigeo 
from models.perfil_usuario import PerfilUsuario
from utils.db import db

mapa_calor = Blueprint('mapa_calor', __name__)

@mapa_calor.route('/api/mapa_calor', methods=['GET'])
def get_mapa_calor():
    try:
        query = db.session.query(
            Ubigeo.X.label('longitude'),
            Ubigeo.Y.label('latitude'),
            TestPuntaje.promedio.label('promedio')
        ).join(Persona, Persona.idubigeo == Ubigeo.idubigeo) \
         .join(Usuario, Usuario.idpersona == Persona.idpersona) \
         .join(PerfilUsuario, PerfilUsuario.idusuario == Usuario.idusuario) \
         .join(TestPuntaje, TestPuntaje.idperfil == PerfilUsuario.idperfil) \
         .all()

        result = [
            {
                'longitude': float(row.longitude),
                'latitude': float(row.latitude),
                'promedio': row.promedio
            }
            for row in query
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
