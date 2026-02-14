from flask_sqlalchemy import SQLAlchemy

import datetime
db= SQLAlchemy()


class Alumnosdb(db.Model):
    __tablename__ = 'alumnos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20))
    apellido = db.Column(db.String(20))
    email = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)