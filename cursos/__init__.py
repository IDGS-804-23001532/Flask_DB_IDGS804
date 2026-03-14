from string import Template

from flask import Blueprint

# Importamos los archivos necesarios para el funcionamiento xd

cursos = Blueprint('cursos', __name__,
                   template_folder='templates',
                   static_folder='static')
from . import routes
