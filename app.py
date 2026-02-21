from flask import Flask, render_template, request, redirect, url_for
from flask import flash 
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from models import db
from models import Alumnosdb


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route("/")
@app.route("/index")
def index():
    create_form = forms.UserForm(request.form)
    alumnos = Alumnosdb.query.all()
    
    return render_template("index.html", form=create_form, alumnos=alumnos)


 
@app.route("/alumnos", methods=['GET', 'POST'])
def alumno():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alumnos = Alumnosdb(nombre=create_form.nombre.data,
                           apellido=create_form.apellido.data, 
                           email=create_form.email.data)
        db.session.add(alumnos)
        db.session.commit()
        
        return redirect(url_for('index'))
    return render_template("alumnos.html", form=create_form)
        
   
   
@app.route("/detalles", methods=['GET', 'POST'])
def detalles():
	create_form = forms.UserForm(request.form)

	if request.method == 'GET':
		id = request.args.get('id')

		alumn1 = db.session.query(Alumnosdb).filter(Alumnosdb.id == id).first()
		id = request.args.get('id')

		nombre = alumn1.nombre
		apellido = alumn1.apellido
		email = alumn1.email
		
	return render_template("detalles.html", id=id, nombre=nombre, apellido=apellido, email=email) 
       
@app.errorhandler(404)
def page_not_found(error):
	return render_template('404.html'), 404



    


if __name__ == '__main__':
 csrf.init_app(app)
 db.init_app(app)	
 with app.app_context():
	 db.create_all()
  
app.run()
    
 

 
 