from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.registro import Registro
from schemas.schemas import RegistroSchema
from services.registro_service import add_registro, get_all_registros, get_registro_by_id, preprocess_date, validate_positive
from database import db
import pandas as pd
import io

registro_bp = Blueprint('registro_bp', __name__)

registro_schema = RegistroSchema()  # Para un solo registro
registros_schema = RegistroSchema(many=True)  # Para múltiples registros

# Endpoint para subir el archivo usando Pandas
@registro_bp.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    allowed_extensions = ['csv', 'txt']
    file_extension = file.filename.split('.').pop().lower()
    if file_extension not in allowed_extensions:
        return jsonify({"error": "Formato de archivo no permitido. Solo se permiten archivos .csv o .txt"}), 400

    try:
        # Leer el archivo usando Pandas
        data = pd.read_csv(io.StringIO(file.stream.read().decode('utf-8')))
    except pd.errors.EmptyDataError:
        return jsonify({"error": "El archivo está vacío"}), 400
    except Exception as e:
        return jsonify({"error": f"Error al leer el archivo: {str(e)}"}), 400

    # Validar que las columnas requeridas existan
    expected_columns = ['id', 'nombre', 'fecha de nacimiento', 'email', 'monto']
    if not all(column in data.columns for column in expected_columns):
        return jsonify({"error": f"El archivo debe contener las columnas: {', '.join(expected_columns)}"}), 400

    errors = []
    processed = []

    # Iterar sobre las filas del DataFrame
    for i, row in data.iterrows():
        try:
            fecha_nacimiento = preprocess_date(row['fecha de nacimiento']).strftime('%Y-%m-%d')
            positive_id = validate_positive(row['id'])

            record = {
                'id': positive_id,
                'nombre': row['nombre'],
                'fecha_nacimiento': fecha_nacimiento,
                'email': row['email'],
                'monto': float(row['monto'])
            }

            # Validar el registro con Marshmallow
            result = registro_schema.load(record)

            # Verificar si el registro ya existe en la base de datos
            if Registro.query.filter_by(id=record['id']).first() or Registro.query.filter_by(email=record['email']).first():
                errors.append(f"Línea {i+1}: Registro duplicado (ID o email ya existe).")
                continue

            # Agregar el registro a la base de datos
            add_registro(result)
            processed.append(f"Línea {i+1}: Procesada con éxito")
        
        except (ValueError, ValidationError) as e:
            error_messages = e.messages if hasattr(e, 'messages') else str(e)
            if isinstance(error_messages, dict):
                error_messages = ', '.join([str(msg).strip("[]'") for msg in error_messages.values()])
            errors.append(f"Línea {i+1}: Error {error_messages}")
            continue

    return jsonify({"processed": processed, "errors": errors}), 200

# Endpoint para obtener todos los registros
@registro_bp.route('/registros', methods=['GET'])
def get_all():
    registros = get_all_registros()  # Obtener todos los registros
    result = registros_schema.dump(registros)  # Serializar los resultados
    return jsonify(result), 200

# Endpoint para obtener un registro por ID
@registro_bp.route('/registros/<int:id>', methods=['GET'])
def get_by_id(id):
    registro = get_registro_by_id(id)  # Buscar el registro por ID
    if not registro:
        return jsonify({"error": "Registro no encontrado"}), 404
    
    result = registro_schema.dump(registro)  # Serializar el resultado
    return jsonify(result), 200
