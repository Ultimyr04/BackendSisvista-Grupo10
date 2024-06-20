from flask import Blueprint, jsonify
from utils.db import db

test_db_bp = Blueprint('test_db', __name__)

@test_db_bp.route('/api/test-db', methods=['GET'])
def test_db():
    try:
        result = db.session.execute('SELECT 1')
        return jsonify({"message": "Connection successful", "result": [row[0] for row in result]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
