from flask import Blueprint, request, jsonify
from models.usuario import Usuario
from models.test_puntaje import TestPuntaje
from models.nivel_ansiedad import NivelAnsiedad
from utils.db import db
from sqlalchemy.exc import IntegrityError

testrealizados_routes = Blueprint('testrealizados_routes', __name__)

@testrealizados_routes.route('/api/testrealizados/estudiantes', methods=['GET'])
def get_estudiantes():
    estudiantes = Usuario.query.filter(Usuario.rol == 'ESTUDIANTE').all()
    return jsonify([estudiante.to_dict() for estudiante in estudiantes])




@testrealizados_routes.route('/api/testrealizados/<int:idusuario>', methods=['GET'])
def get_tests(idusuario):
    tests = TestPuntaje.query.filter_by(idperfil=idusuario).all()
    resultados = []
    for test in tests:
        nivel = NivelAnsiedad.query.get(test.idnivelansiedad)
        puntaje = test.totaltest1 if test.idtipotest == 1 else (test.totaltest2 if test.idtipotest == 2 else test.totaltest3)
        resultados.append({
            'tipoTest': test.idtipotest,
            'fecha': test.fecha.strftime('%Y-%m-%d'),
            'puntaje': puntaje,
            'nivel': nivel.nivel
        })
    return jsonify(resultados)



@testrealizados_routes.route('/api/testrealizado/actualizarTest/<int:id_test>', methods=['POST'])
def update_test(idtipotest):
    data = request.get_json()
    test = TestPuntaje.query.get(idtipotest)
    if 'puntaje' in data:
        if test.idtipotest == 1:
            test.totaltest1 = data['puntaje']
        elif test.idtipotest == 2:
            test.totaltest2 = data['puntaje']
        elif test.idtipotest == 3:
            test.totaltest3 = data['puntaje']
        
        # Recalcular el promedio si es necesario
        if all([test.totaltest1, test.totaltest2, test.totaltest3]):
            test.promedio = (test.totaltest1 + test.totaltest2 + test.totaltest3) / 3
            nivelansiedad = NivelAnsiedad.query.filter(NivelAnsiedad.minrespuesta <= test.promedio, NivelAnsiedad.maxrespuesta >= test.promedio).first()
            if nivelansiedad:
                test.idnivelansiedad = nivelansiedad.idnivelansiedad

        db.session.commit()
        return jsonify({'message': 'Puntaje actualizado'}), 200
    return jsonify({'error': 'Puntaje no proporcionado'}), 400
