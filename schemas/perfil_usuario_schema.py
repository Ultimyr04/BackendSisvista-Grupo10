from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from models.perfil_usuario import PerfilUsuario

class PerfilUsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = PerfilUsuario
        fields = ('idperfil', 'idusuario', 'imagenperfil', 'observaciones')
        load_instance = True

perfil_usuario_schema = PerfilUsuarioSchema()
perfiles_usuario_schema = PerfilUsuarioSchema(many=True)
