from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.respuestas import Respuesta

class NivelHamaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Respuesta
        fields = ('idrespuesta', 'idtipotest', 'textorespuesta')
        load_instance = True

respuesta_schema = NivelHamaSchema()
respuestas_schema = NivelHamaSchema(many=True)
