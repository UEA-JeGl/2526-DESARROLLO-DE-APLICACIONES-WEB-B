from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre completo",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    correo = StringField(
        "Correo electrónico",
        validators=[
            DataRequired(message="El correo electrónico es obligatorio."),
            Email(message="Ingrese un correo electrónico válido.")
        ]
    )

    tipo = SelectField(
        "Tipo de cliente",
        choices=[
            ("", "Seleccione un tipo"),
            ("Estudiante", "Estudiante"),
            ("Emprendedor", "Emprendedor"),
            ("Empresa", "Empresa")
        ],
        validators=[
            DataRequired(message="Debe seleccionar un tipo de cliente.")
        ]
    )

    submit = SubmitField("Registrar cliente")

