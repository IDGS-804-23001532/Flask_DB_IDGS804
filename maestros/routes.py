from . import maestros 
from flask import  render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from models import Maestros, Alumnosdb


@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil del maestro: {nombre}"


@maestros.route('/maestros', methods=['GET', 'POST'])
@maestros.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    maestros = Maestros.query.all()
    return render_template("maestros2/listadoMaestros.html", form=create_form, maestros=maestros)


@maestros.route('/maestro/nuevo', methods = ['GET', 'POST'])
@maestros.route('/agregar')
def agregar():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
       maestros = Maestros(
           nombre = create_form.nombre.data,
           apellidos = create_form.apellidos.data,
           especialidad = create_form.especialidad.data,
           email = create_form.email.data
           
       )