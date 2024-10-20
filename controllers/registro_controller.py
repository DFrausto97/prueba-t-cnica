
from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from models.registro import Registro
from schemas.schemas import RegistroSchema
from services.registro_service import add_registro, get_all_registros, get_registro_by_id, preprocess_date, validate_positive
from database import db


registro_bp = Blueprint('registro_bp', __name__)


registro_schema = RegistroSchema()  # Para un solo registro
registros_schema = RegistroSchema(many=True)  # Para múltiples registros

# Endpoint para subir el archivo
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

    errors = []
    processed = []
    for i, line in enumerate(file.readlines(), start=1):
        try:
            values = line.decode('utf-8').strip().split(',')

            fecha_nacimiento = preprocess_date(values[2]).strftime('%Y-%m-%d')

            positive_id = validate_positive(values[0])

            data = {
                'id': positive_id,
                'nombre': values[1],
                'fecha_nacimiento': fecha_nacimiento,
                'email': values[3],
                'monto': float(values[4])
            }

            result = registro_schema.load(data)

            # Verificar si el registro ya existe en la base de datos por ID o email
            if Registro.query.filter_by(id=data['id']).first() or Registro.query.filter_by(email=data['email']).first():
                errors.append(f"Línea {i}: Registro duplicado (ID o email ya existe).")
                continue  # Ignorar este registro y pasar al siguiente

            add_registro(result)
            processed.append(f"Línea {i}: Procesada con éxito")
        except (ValueError, ValidationError) as e:
            error_messages = e.messages if hasattr(e, 'messages') else str(e)
            if isinstance(error_messages, dict):
                error_messages = ', '.join([str(msg).strip("[]'") for msg in error_messages.values()])
            errors.append(f"Línea {i}: Error {error_messages}")
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