from marshmallow import  ValidationError
from datetime import datetime
from models.registro import Registro
from database import db

def no_special_characters(value):
    import re
    if re.search(r'[^a-zA-Z0-9 ]', value):
        raise ValidationError("El campo contiene caracteres especiales no permitidos.")
    
def validate_integer(value):
    if not isinstance(value, int):
            raise ValidationError("El ID debe ser un número entero.")
    
def validate_positive(value):
    if int(value) <= 0:
            raise ValidationError("El ID debe ser un número entero positivo.")
    return value

# Función para convertir fechas a formato YYYY-MM-DD
def preprocess_date(date_str):
    try:
        # Intentar DD-MM-YYYY
        return datetime.strptime(date_str, '%d-%m-%Y').date()
    except ValueError:
        try:
            # Intentar YYYY/MM/DD
            return datetime.strptime(date_str, '%Y/%m/%d').date()
        except ValueError:
            raise ValidationError("Formato de fecha inválido.")
        
def add_registro(data):
    """Inserta un registro en la base de datos."""
    registro = Registro(**data)
    db.session.add(registro)
    db.session.commit()

def get_all_registros():
    """Obtiene todos los registros."""
    return Registro.query.all()

def get_registro_by_id(id):
    """Obtiene un registro por ID."""
    return Registro.query.get(id)