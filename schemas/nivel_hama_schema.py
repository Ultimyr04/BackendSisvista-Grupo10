from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.nivel_hama import NivelHama

class NivelHamaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NivelHama
        fields = ('idnivelansiedad', 'minrespuesta', 'maxrespuesta', 'nivel')
        load_instance = True

nivel_hama_schema = NivelHamaSchema()
niveles_hama_schema = NivelHamaSchema(many=True)
