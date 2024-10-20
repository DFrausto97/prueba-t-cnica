from flask import Flask, request, jsonify
from marshmallow import ValidationError
from database import init_db, db
from models import Registro
from schemas import RegistroSchema
from datetime import datetime

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

registro_schema = RegistroSchema()  # Para un solo registro
registros_schema = RegistroSchema(many=True)  # Para múltiples registros

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

registro_schema = RegistroSchema()  # Para un solo registro
registros_schema = RegistroSchema(many=True)  # Para múltiples registros

# Endpoint para subir el archivo
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    errors = []
    processed = []
    for i, line in enumerate(file.readlines(), start=1):
        try:
            values = line.decode('utf-8').strip().split(',')

            id_validation = validate_positive(int(values[0]))

            fecha_nacimiento = preprocess_date(values[2]).strftime('%Y-%m-%d')

            data = {
                'id': id_validation,
                'nombre': values[1],
                'fecha_nacimiento': fecha_nacimiento,  # Convertida a string
                'email': values[3],
                'monto': float(values[4])
            }

            result = registro_schema.load(data)

            # Verificar si el registro ya existe en la base de datos por ID o email
            if Registro.query.filter_by(id=data['id']).first() or Registro.query.filter_by(email=data['email']).first():
                errors.append(f"Línea {i}: Registro duplicado (ID o email ya existe).")
                continue  # Ignorar este registro y pasar al siguiente

            registro = Registro(**result)
            db.session.add(registro)
            db.session.commit()
            processed.append(f"Línea {i}: Procesada con éxito")
        except (ValueError, ValidationError) as e:
            errors.append(f"Línea {i}: Error {str(e)}")
            continue

    return jsonify({"processed": processed, "errors": errors}), 200






# Endpoint para obtener todos los registros
@app.route('/registros', methods=['GET'])
def get_all():
    registros = Registro.query.all()  # Obtener todos los registros
    result = registros_schema.dump(registros)  # Serializar los resultados
    return jsonify(result), 200

# Endpoint para obtener un registro por ID
@app.route('/registros/<int:id>', methods=['GET'])
def get_by_id(id):
    registro = Registro.query.get(id)  # Buscar el registro por ID
    if not registro:
        return jsonify({"error": "Registro no encontrado"}), 404
    
    result = registro_schema.dump(registro)  # Serializar el resultado
    return jsonify(result), 200

if __name__ == '__main__':
    app.run(debug=True)
