from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.test_respuesta import TestRespuesta

class TestRespuestaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TestRespuesta
        fields = ('idtestrespuesta','idusuario','idtipotest', 'pregunta', 'respuesta')
        load_instance = True

test_respuesta_schema = TestRespuestaSchema()
tests_respuesta_schema = TestRespuestaSchema(many=True)
