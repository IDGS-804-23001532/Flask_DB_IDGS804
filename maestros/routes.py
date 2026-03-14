import re

from wtforms.validators import email

from . import maestros 
from flask import  render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from models import Maestros, Alumnosdb, db


@maestros.route('/perfil/<nombre>')
def perfil(nombre):
    return f"Perfil del maestro: {nombre}"

# Listar maestros                                                
@maestros.route('/maestros', methods=['GET', 'POST'])
def index():
    create_form = forms.MaestroForm(request.form)
    maestros = Maestros.query.all()
    
    return render_template("maestros2/listadoMaestros.html",
                           form=create_form,maestros=maestros)
# Agregar un maestro
@maestros.route('/maestrosAgregar', methods = ['GET', 'POST']) #Esta ruta es para agregar maestros, se llama desde el boton agregar del listado de maestros
@maestros.route('/agregar', methods = ['GET', 'POST']) #ruta para agregar maestros, se llama desde el formulario de agregar maestro
def agregar():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'POST' and create_form.validate():
       maestros2 = Maestros(
                matricula = create_form.matricula.data,
                nombre = create_form.nombre.data,
                apellidos = create_form.apellidos.data,
                especialidad = create_form.especialidad.data,
                email = create_form.email.data)
       db.session.add(maestros2)
       db.session.commit()
       flash('Maestro agregado', 'success')
       return redirect(url_for('maestros.index')) #Redirecciona al listado de maestros despues de agregar un maestro
    return render_template("maestros2/maestro.html", form=create_form) #Renderiza el formulario para agregar un maestro

#Modificar el maestro xd
@maestros.route('/modificarMaestro', methods = ['GET', 'POST'])
def modificar():
    create_form = forms.MaestroForm(request.form)
    if request.method ==  'GET':
        matricula= request.args.get('matricula')
        
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if not maes1:
            flash('Maestro no encontrado', 'error')
            return redirect(url_for('maestros.index'))
        
        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
        
    if request.method == 'POST':
        matricula = create_form.matricula.data
        if not matricula: # Fallback if for some reason the form data is missing
            matricula = request.args.get('matricula')
            
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if not maes1:
            flash('Maestro no encontrado para modificar', 'error')
            return redirect(url_for('maestros.index'))
        
        maes1.nombre = create_form.nombre.data
        maes1.apellidos = create_form.apellidos.data
        maes1.especialidad = create_form.especialidad.data
        maes1.email = create_form.email.data
        
        db.session.add(maes1)
        db.session.commit()
        flash('Maestro modificado', 'success')
        return redirect(url_for('maestros.index')) #Redirecciona al listado de maestros despues de modificar un maestro
    return render_template("maestros2/modificar.html", form=create_form) #Renderiza el formulario para modificar un maestro


    #Detalle maestro
@maestros.route('/detalleMaestro',methods =['GET'])
def detalle():
    create_form = forms.MaestroForm(request.form)
    
    if request.method == 'GET':
       matricula = request.args.get('matricula')
    
       maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
       if not maes1:
           flash('Maestro no encontrado', 'error')
           return redirect(url_for('maestros.index'))
    
       matricula =request.args.get('matricula')
       nombre = maes1.nombre
       apellidos = maes1.apellidos
       especialidad = maes1.especialidad
       email = maes1.email
    return render_template("maestros2/detallesMaes.html", form=create_form, matricula=matricula, nombre=nombre, apellidos=apellidos, especialidad=especialidad, email=email)


 #Eliminar maestro
@maestros.route('/eliminarMaestro', methods = ['GET', 'POST'])
def eliminar():
    create_form = forms.MaestroForm(request.form)
    if request.method == 'GET':
        
        matricula = request.args.get('matricula')
        
        maes1 = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if not maes1:
            flash('Maestro no encontrado', 'error')
            return redirect(url_for('maestros.index'))
        
        create_form.matricula.data = maes1.matricula
        create_form.nombre.data = maes1.nombre
        create_form.apellidos.data = maes1.apellidos
        create_form.especialidad.data = maes1.especialidad
        create_form.email.data = maes1.email
        
    if request.method == 'POST':
        matricula = create_form.matricula.data
        if not matricula: # Fallback just in case
            matricula = request.args.get('matricula')
            
        maes1 = Maestros.query.get(matricula)
        if not maes1:
            flash('Maestro no encontrado para eliminar', 'error')
            return redirect(url_for('maestros.index'))
            
        db.session.delete(maes1)
        db.session.commit()
        flash('Maestro eliminado', 'success')
        return redirect(url_for('maestros.index'))
    return render_template("maestros2/eliminar.html", form=create_form)
