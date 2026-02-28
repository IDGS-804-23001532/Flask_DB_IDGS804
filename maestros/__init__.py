from flask import Blueprint

# Importamos los archivos necesarios para el funcionamiento del blueprint
maestros = Blueprint('maestros', __name__, 
                     template_folder='templates',
                     static_folder='static')
from . import routes