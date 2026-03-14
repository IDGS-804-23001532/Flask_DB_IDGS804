from wtforms import Form, SelectField, StringField, validators
from wtforms import StringField, PasswordField, EmailField, validators,  IntegerField
from flask_wtf import FlaskForm


class AlumnoForm(Form):
    id = IntegerField('id', [validators.Optional()])
    nombre = StringField('Nombre', [ validators.DataRequired(message='El nombre es requerido'),
                                    validators.Length(min=4, max=20, message='El nombre debe tener entre 4 y 20 caracteres')]
                         )
    apellidos = StringField('apellidos',[validators.DataRequired(message='El apeliido es requerido')])
    email = EmailField('email', [validators.DataRequired(message='El email es requerido'),
                                        validators.Email(message='El email no es valido')])
    telefono = StringField('telefono', [validators.DataRequired(message='El telefono es requerido')])
    
class MaestroForm(Form):
    matricula = IntegerField('matricula', [validators.DataRequired(message='La matricula es requerida')])
    nombre = StringField('Nombre', [ validators.DataRequired(message='El nombre es requerido'),
                                    validators.Length(min=4, max=20, message='El nombre debe tener entre 4 y 20 caracteres')]
                         )
    apellidos = StringField('apellidos',[validators.DataRequired(message='El apeliido es requerido')])
    especialidad = StringField('especialidad', [ validators.DataRequired(message='La especialidad es requerida'),
                                    validators.Length(min=4, max=20, message='La especialidad debe tener entre 4 y 20 caracteres')]
                            )
    email = EmailField('email', [validators.DataRequired(message='El email es requerido'),
                                        validators.Email(message='El email no es valido')])
    
    
    
    
class CursoForm(FlaskForm):

    id = IntegerField(
        'id',
        [validators.DataRequired(message='El id es requerido')]
    )

    nombre = StringField(
        'Nombre',
        [
            validators.DataRequired(message='El nombre es requerido'),
            validators.Length(min=4, max=20, message='El nombre debe tener entre 4 y 20 caracteres')
        ]
    )

    descripcion = StringField(
        'descripcion',
        [
            validators.DataRequired(message='La descripcion es requerida'),
            validators.Length(min=4, max=200, message='La descripcion debe tener entre 4 y 200 caracteres')
        ]
    )

    maestro_id = SelectField('Maestro', [validators.DataRequired(message='Seleccione un maestro')], coerce=int)


class InscripcionForm(FlaskForm):
    id = IntegerField('id', [validators.Optional()])
    
    curso_id = SelectField(
        'curso_id',
        [validators.DataRequired(message='El curso_id es requerido')],
        coerce=int
    )
    alumno_id = SelectField(
        'alumno_id',
        [validators.DataRequired(message='El alumno_id es requerido')],
        coerce=int
    )
   
    
