from datetime import date
from database import db

class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    monto = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Registro {self.nombre}>'
