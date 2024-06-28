from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.test_db import test_db_bp
from routes.user_routes import user_bp  # Asegúrate de importar el blueprint correctamente
from routes.register_routes import register_bp
from config import Config
from utils.db import db

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

app.config["SQLALCHEMY_DATABASE_URI"] = Config.DATABASE_CONNECTION_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800

# no cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db.init_app(app)
jwt = JWTManager(app)

app.secret_key = 'clavesecreta123'

app.register_blueprint(test_db_bp)
app.register_blueprint(user_bp)  # Registra el blueprint
app.register_blueprint(register_bp)

if __name__ == '__main__':
    app.run(port=5000)
