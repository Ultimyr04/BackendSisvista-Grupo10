from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.preguntas import Pregunta

class NivelHamaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pregunta
        fields = ('idpregunta', 'idtipotest', 'textopregunta')
        load_instance = True

pregunta_schema = NivelHamaSchema()
preguntas_schema = NivelHamaSchema(many=True)
