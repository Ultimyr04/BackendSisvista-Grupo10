from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from utils.db import db

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/api/user_routes/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        usuario = data.get('usuario')
        contrasena = data.get('contrasena')
        user = User.query.filter_by(nickusuario=usuario).first()

        # Verificación con hash
        if user and user.check_password(contrasena):
            access_token = create_access_token(identity={'id': user.idusuario, 'nickusuario': user.nickusuario})
            return jsonify({'token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500


@user_routes.route('/api/user_routes/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_list = [{'id': user.idusuario, 'nickusuario': user.nickusuario} for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}),500
