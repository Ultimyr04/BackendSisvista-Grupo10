from flask import Blueprint, request, jsonify
from models.user import User
from utils.db import db
import logging

register_user = Blueprint('user_register', __name__)

@register_user.route('/api/user_register/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        logging.debug(f'Received data: {data}')
        
        if data is None:
            logging.error('No JSON data received')
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        new_user = User(
            nombres=data.get('nombres'),
            apellidos=data.get('apellidos'),
            ciudad=data.get('ciudad'),
            email=data.get('email'),
            telefono=data.get('telefono'),
            genero=data.get('genero'),
            fechanacimiento=data.get('fechanacimiento'),
            nickusuario=data.get('nickusuario'),
            rol=data.get('rol')
        )
        new_user.set_password(data.get('contrasena'))
        
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error: {str(e)}')
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500