from wtforms import Form, StringField, validators
from wtforms import StringField, PasswordField, EmailField, validators,  IntegerField
from flask_wtf import FlaskForm


class UserForm(Form):
    id= IntegerField('id', [validators.NumberRange(min=1, max=20, message='valor no valido')])
    nombre = StringField('Nombre', [ validators.DataRequired(message='El nombre es requerido'),
                                    validators.Length(min=4, max=20, message='El nombre debe tener entre 4 y 20 caracteres')]
                         )
    apellidos = StringField('apellidos',[validators.DataRequired(message='El apeliido es requerido')])
    email = EmailField('email', [validators.DataRequired(message='El email es requerido'),
                                        validators.Email(message='El email no es valido')])
    telefono = StringField('telefono', [validators.DataRequired(message='El telefono es requerido')])
    
    especialidad = StringField('especialidad', [ validators.DataRequired(message='La especialidad es requerida'),
                                    validators.Length(min=4, max=20, message='La especialidad debe tener entre 4 y 20 caracteres')]
                            )
    matricula = IntegerField('matricula', [validators.NumberRange(min=5, message='valor no valido')])