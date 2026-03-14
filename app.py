from flask import Flask, render_template, request, redirect, url_for
from flask import flash 
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from models import db
from models import Alumnosdb, Maestros, Cursos, Inscripciones
from flask_migrate import Migrate
from maestros.routes import maestros 
from cursos.routes import cursos
from inscripciones.routes import inscripciones

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.register_blueprint(maestros)
app.register_blueprint(cursos)
app.register_blueprint(inscripciones)

db.init_app(app)	
csrf = CSRFProtect()
migrate = Migrate(app, db)


@app.route("/")
@app.route("/Inicio")
def index():
    create_form = forms.AlumnoForm(request.form)
    alumnos = Alumnosdb.query.all()
    alumnos_count = Alumnosdb.query.count()
    maestros_count = Maestros.query.count()
    cursos_count = Cursos.query.count()
    inscripciones_count = Inscripciones.query.count()
    modulos = [
        {"label": "Alumnos", "url": "/listarAlumnos", "tag": "Módulo", "desc": "Registro y consulta de alumnos", "count": alumnos_count},
        {"label": "Maestros", "url": "/maestros", "tag": "Módulo", "desc": "Catálogo de docentes activos", "count": maestros_count},
        {"label": "Cursos", "url": "/cursos", "tag": "Módulo", "desc": "Administración de cursos disponibles", "count": cursos_count},
        {"label": "Inscripciones", "url": "/inscripciones", "tag": "Módulo", "desc": "Inscribir alumnos a cursos y consultar registros", "count": inscripciones_count},
        {"label": "Grupos", "url": "/grupos", "tag": "Módulo", "desc": "Distribución de alumnos por curso"},
        {"label": "Buscar Alumnnos", "url": "/BuscarAlumnos","tag": "Módulo", "desc": "Buscar alumnos para visualizar sus cursos"}
    ]
    return render_template(
        "Inicio.html",
        form=create_form,
        alumnos=alumnos,
        alumnos_count=alumnos_count,
        maestros_count=maestros_count,
        cursos_count=cursos_count,
        inscripciones_count=inscripciones_count,
        modulos=modulos,
    )


@app.route("/listarAlumnos")
def lista_alumnos():
	alumnos = Alumnosdb.query.all()
	return render_template("index.html", alumnos=alumnos)
 
@app.route("/alumnos", methods=['GET', 'POST'])
def alumno():
    create_form = forms.AlumnoForm(request.form)
    if request.method == 'POST' and create_form.validate():
        alumnos = Alumnosdb(nombre=create_form.nombre.data,
                           apellidos=create_form.apellidos.data, 
                           email=create_form.email.data,
                           telefono=create_form.telefono.data)
        db.session.add(alumnos)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template("alumnos.html", form=create_form)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
	create_form = forms.AlumnoForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnosdb).filter(Alumnosdb.id == id).first()

		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alumn1.nombre
		create_form.apellidos.data = alumn1.apellidos
		create_form.telefono.data = alumn1.telefono
		create_form.email.data = alumn1.email
	
	if request.method == 'POST':
		id = create_form.id.data
		alumn1 = db.session.query(Alumnosdb).filter(Alumnosdb.id == id).first()

		alumn1.id = id
		alumn1.nombre = create_form.nombre.data
		alumn1.apellidos = create_form.apellidos.data
		alumn1.telefono = create_form.telefono.data
		alumn1.email = create_form.email.data
		
		db.session.add(alumn1)
		db.session.commit()
		
		return redirect(url_for("index")) 
	return render_template("modificar.html", form=create_form)


	

   
@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
	create_form = forms.AlumnoForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnosdb).filter(Alumnosdb.id == id).first()
		id = request.args.get('id')

		nombre = alumn1.nombre
		apellidos = alumn1.apellidos
		email = alumn1.email
		telefono = alumn1.telefono
		
	return render_template("detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email, telefono=telefono) 
       
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404


@app.route("/eliminar", methods=['GET', 'POST'])  
def eliminar():
	create_form = forms.AlumnoForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnosdb).filter(Alumnosdb.id == id).first()

		create_form.id.data = request.args.get('id')
		create_form.nombre.data = alumn1.nombre
		create_form.apellidos.data = alumn1.apellidos
		create_form.email.data = alumn1.email   
		create_form.telefono.data = alumn1.telefono
	
	if request.method == 'POST':
		id = create_form.id.data
		alumn1 = Alumnosdb.query.get(id)
		db.session.delete(alumn1)
		db.session.commit()
		
		return redirect(url_for("index")) 
	return render_template("eliminar.html", form=create_form)
	
@app.route("/BuscarAlumnos")
def BuscarAlumno():
    # 1. Obtenemos el ID que viene del formulario (si existe)
    alumno_id = request.args.get('alumno_id')
    
    # 2. Traemos todos los alumnos para llenar el <select>
    alumnos_db = Alumnosdb.query.all() 
    
    alumno_seleccionado = None
    inscripciones = []

    # 3. Si el usuario seleccionó a alguien, buscamos sus datos
    if alumno_id:
        alumno_seleccionado = Alumnosdb.query.get(alumno_id)
        if alumno_seleccionado:
            # Traemos las inscripciones para ver sus cursos y profes
            inscripciones = Inscripciones.query.filter_by(alumno_id=alumno_id).all()

    return render_template("buscarAlumno.html", 
                           alumnos_db=alumnos_db, 
                           alumno_seleccionado=alumno_seleccionado, 
                           inscripciones=inscripciones,
                           selected_id=alumno_id)
    


if __name__ == '__main__':
 csrf.init_app(app)
 with app.app_context():
	 db.create_all()
  
app.run()
    
 

 
 
