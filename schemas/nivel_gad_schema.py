from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.nivel_gad import NivelGad

class NivelGadSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = NivelGad
        fields = ('idnivelansiedad', 'minrespuesta', 'maxrespuesta', 'nivel')
        load_instance = True

nivel_gad_schema = NivelGadSchema()
niveles_gad_schema = NivelGadSchema(many=True)
