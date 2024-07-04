import logging
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.test_db import test_db_bp
from routes.test_puntaje_routes import test_puntaje_routes
from routes.test_respuesta_routes import test_respuesta_routes
from routes.mapacalor_routes import mapa_calor
from routes.user_routes import user_bp
from routes.register_routes import register_bp
from routes.formulario_routes import formulario
from config import Config
from utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.exceptions import HTTPException

# Configurar registro de errores
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800

# No cachear archivos
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)
jwt = JWTManager(app)

app.secret_key = 'clavesecreta123'

# Registra los blueprints
app.register_blueprint(test_db_bp)
app.register_blueprint(user_bp) #Verificacion de un usuario y contraseña en el LOGIN
app.register_blueprint(register_bp) #Registrar un usuario nuevo 
app.register_blueprint(formulario) #Extraer las preguntas y respuestas
app.register_blueprint(test_respuesta_routes) #Guarda las respuestas de un usuario
app.register_blueprint(test_puntaje_routes)

app.register_blueprint(mapa_calor)

@app.errorhandler(Exception)
def handle_exception(e):
    """Maneja todas las excepciones no controladas."""
    logger.error(f"An exception occurred: {str(e)}")
    return jsonify(error=str(e)), 500


@app.errorhandler(SQLAlchemyError)
def handle_database_error(e):
    """Maneja los errores de SQLAlchemy."""
    logger.error(f"A database error occurred: {str(e)}")
    db.session.rollback()  # Rollback en caso de error de base de datos
    return jsonify(error="Database error"), 500


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """Maneja las excepciones HTTP."""
    logger.error(f"An HTTP error occurred: {str(e)}")
    return jsonify(error=str(e)), e.code


if __name__ == '__main__':
    app.run(port=5000)
