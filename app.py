from flask import Flask
from config import Config
from database import db
from flask_migrate import Migrate

# Crear instancia de la aplicación Flask
app = Flask(__name__)
app.config.from_object(Config)

# Inicializar la base de datos y las migraciones
db.init_app(app)
migrate = Migrate(app, db)

# Registrar blueprints aquí si es necesario
from controllers.registro_controller import registro_bp
app.register_blueprint(registro_bp)

# Iniciar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
