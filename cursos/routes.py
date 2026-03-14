import re

from wtforms.validators import email

import maestros

from . import cursos  
from flask import  render_template, request, redirect, session, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from models import Cursos, Maestros, Alumnosdb, db


@cursos.route('/maluma/<nombre>')
def perfil(nombre):
    return f"Perfil del curso: {nombre}"



@cursos.route('/cursos')
def list_cursos():
    cursos = Cursos.query.all()
    return render_template('cursos/listaCursos.html', cursos = cursos)

@cursos.route('/agregarCurso', methods = ['GET', 'POST'])
@cursos.route('/agregar', methods = ['GET', 'POST'])
def agregar():
    create_form = forms.CursoForm()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in Maestros.query.all()]
    if request.method == 'POST' and create_form.validate():
       existing = db.session.query(Cursos).filter(
           Cursos.nombre == create_form.nombre.data,
           Cursos.maestro_id == create_form.maestro_id.data
       ).first()
       if existing:
           flash('Ya existe un curso con ese nombre para ese maestro')
           return render_template("cursos/cursos.html", form=create_form)
       cursos2 = Cursos(
                nombre = create_form.nombre.data,
                descripcion = create_form.descripcion.data,
                maestro_id = create_form.maestro_id.data)
       db.session.add(cursos2)
       db.session.commit()
       flash('Curso creado', 'success')
       return redirect(url_for('cursos.list_cursos')) #Redirecciona al listado de cursos despues de agregar un curso
    return render_template("cursos/cursos.html", form=create_form) #Renderiza el formulario para agregar un curso


@cursos.route('/modificarCurso', methods=['GET','POST'])
def modificarCurso():
    form = forms.CursoForm()
    
    maestros = db.session.query(Maestros).all()
    form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]
    
    if request.method == 'GET':

        id = request.args.get('id')

        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        form.id.data = curso.id
        form.nombre.data = curso.nombre
        form.descripcion.data = curso.descripcion
        form.maestro_id.data = curso.maestro_id

    if request.method == 'POST' and form.validate():

        curso = db.session.query(Cursos).filter(Cursos.id == form.id.data).first()

        curso.nombre = form.nombre.data
        curso.descripcion = form.descripcion.data
        curso.maestro_id = form.maestro_id.data

        db.session.commit()
        flash('Curso modificado', 'success')

        return redirect(url_for('cursos.list_cursos'))
    
    print(form.errors)

    return render_template('cursos/modificar.html', form=form)


@cursos.route('/detalleCurso', methods=['GET'])
def detalleCurso():
    id = request.args.get('id')
    curso = db.session.query(Cursos).filter(Cursos.id == id).first() 
    nombre = curso.nombre
    descripcion = curso.descripcion
    maestro_rel = curso.maestro
    alumno = db.session.query(Alumnosdb).filter(Alumnosdb.cursos.any(id=id)).all()
    return render_template('cursos/detalle.html', id=id, nombre=nombre, descripcion=descripcion, maestro_id=maestro_rel, alumnos=alumno)

@cursos.route('/EliminarCurso', methods=['GET','POST'])
def eliminarCurso():
    create_form = forms.CursoForm()

    maestros = db.session.query(Maestros).all()
    create_form.maestro_id.choices = [(m.matricula, m.nombre) for m in maestros]

    if request.method == 'GET':
        id = request.args.get('id')
        curso = db.session.query(Cursos).filter(Cursos.id == id).first()

        create_form.id.data = curso.id
        create_form.nombre.data = curso.nombre
        create_form.descripcion.data = curso.descripcion
        create_form.maestro_id.data = curso.maestro_id

    if request.method == 'POST':
        id = create_form.id.data

        cursos1 = Cursos.query.get(id)

        if cursos1 is not None:
            db.session.delete(cursos1)
            db.session.commit()
            flash('Curso eliminado', 'success')

        return redirect(url_for('cursos.list_cursos'))

    return render_template("cursos/eliminar.html", form=create_form)
    

@cursos.route("/grupos")
def list_grupos():
    cursos_list = Cursos.query.all()
    selected_id = request.args.get('curso_id')
    selected_curso = Cursos.query.get(selected_id) if selected_id else None
    alumnos = selected_curso.alumnos if selected_curso else []
    return render_template("cursos/grupos.html", cursos=cursos_list, selected_curso=selected_curso, alumnos=alumnos, selected_id=selected_id)



