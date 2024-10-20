from flask import Flask, request, render_template
from marshmallow import ValidationError
from config import Config
from database import init_db
from controllers.registro_controller import registro_bp



app = Flask(__name__)

# Configuración de la base de datos
app.config.from_object(Config)
init_db(app)

# Registrar los blueprints
app.register_blueprint(registro_bp)

if __name__ == '__main__':
    app.run(debug=True)
