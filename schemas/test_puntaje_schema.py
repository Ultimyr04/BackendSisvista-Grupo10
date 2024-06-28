from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.test_puntaje import TestPuntaje

class TestPuntajeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = TestPuntaje
        fields = ('idpuntajes','totaltest1', 'totaltest2', 'totaltest3', 'idnivelansiedad','idperfil')
        load_instance = True

test_puntaje_schema = TestPuntajeSchema()
tests_puntaje_schema = TestPuntajeSchema(many=True)
