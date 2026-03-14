from . import inscripciones
from flask import render_template, request, redirect, url_for, flash
from models import Inscripciones, Alumnosdb, Cursos, db
import forms


@inscripciones.route('/inscripciones')
def list_inscripciones():
    inscripciones_list = Inscripciones.query.all()
    return render_template('inscripciones/listaInscripciones.html', inscripciones=inscripciones_list)


@inscripciones.route('/inscripciones/agregar', methods=['GET', 'POST'])
def agregar_inscripcion():
    form = forms.InscripcionForm()
    form.alumno_id.choices = [(a.id, a.nombre) for a in Alumnosdb.query.all()]
    form.curso_id.choices = [(c.id, c.nombre) for c in Cursos.query.all()]
    if request.method == 'POST' and form.validate():
        dup = db.session.query(Inscripciones).filter(
            Inscripciones.alumno_id == form.alumno_id.data,
            Inscripciones.cursos_id == form.curso_id.data
        ).first()
        if dup:
            flash('El alumno ya está inscrito en ese curso', 'error')
            return render_template('inscripciones/inscripciones.html', form=form)
            
        insc = Inscripciones(alumno_id=form.alumno_id.data, cursos_id=form.curso_id.data)
        db.session.add(insc)
        db.session.commit()
        flash('Inscripción creada', 'success')
        return redirect(url_for('inscripciones.list_inscripciones'))
    return render_template('inscripciones/inscripciones.html', form=form)


@inscripciones.route('/modificarInscripcion', methods=['GET','POST'])
def modificarInscripcion():
    form = forms.InscripcionForm()
    form.alumno_id.choices = [(a.id, a.nombre) for a in Alumnosdb.query.all()]
    form.curso_id.choices = [(c.id, c.nombre) for c in Cursos.query.all()]
    if request.method == 'GET':

        id = request.args.get('id')

        inscripcion = db.session.query(Inscripciones).filter(Inscripciones.id == id).first()

        form.id.data = inscripcion.id
        form.alumno_id.data = inscripcion.alumno_id
        form.curso_id.data = inscripcion.cursos_id

    if request.method == 'POST' and form.validate():

        inscripcion = db.session.query(Inscripciones).filter(Inscripciones.id == form.id.data).first()

        inscripcion.alumno_id = form.alumno_id.data
        inscripcion.cursos_id = form.curso_id.data

        db.session.commit()
        flash('Inscripción modificada', 'success')

        return redirect(url_for('inscripciones.list_inscripciones'))
    
    print(form.errors)

    return render_template('inscripciones/modificar.html', form=form)


@inscripciones.route('/detalleInscripcion', methods=['GET'])
def detalleInscripcion():
    id = request.args.get('id')
    inscripcion = db.session.query(Inscripciones).filter(Inscripciones.id == id).first()
    return render_template('inscripciones/detalle.html', inscripcion=inscripcion)

@inscripciones.route('/EliminarInscripcion', methods=['GET','POST'])
def eliminarInscripcion():
    create_form = forms.InscripcionForm()
    create_form.alumno_id.choices = [(a.id, a.nombre) for a in Alumnosdb.query.all()]
    create_form.curso_id.choices = [(c.id, c.nombre) for c in Cursos.query.all()]
    if request.method == 'GET':
        id = request.args.get('id')
        inscripcion = db.session.query(Inscripciones).filter(Inscripciones.id == id).first()

        create_form.id.data = inscripcion.id
        create_form.alumno_id.data = inscripcion.alumno_id
        create_form.curso_id.data = inscripcion.cursos_id

    if request.method == 'POST':
        id = create_form.id.data

        inscripcion1 = Inscripciones.query.get(id)

        if inscripcion1 is not None:
            db.session.delete(inscripcion1)
            db.session.commit()
            flash('Inscripción eliminada', 'success')

        return redirect(url_for('inscripciones.list_inscripciones'))

    return render_template("inscripciones/eliminar.html", form=create_form)
