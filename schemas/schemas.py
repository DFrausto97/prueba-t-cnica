from marshmallow import Schema, fields
from services.registro_service import no_special_characters



class RegistroSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "El id es obligatorio.", "invalid": "Debe ser un numero entero."})
    nombre = fields.Str(required=True, validate=no_special_characters)
    fecha_nacimiento = fields.DateTime(required=True, format='%Y-%m-%d')  # Especifica el formato
    email = fields.Email(required=True, error_messages={"required": "El correo electrónico es obligatorio.", "invalid": "Correo electrónico no válido."})
    monto = fields.Float(required=True)