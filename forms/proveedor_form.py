from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProveedorForm(FlaskForm):

    empresa = StringField(
        "Nombre de la empresa",
        validators=[
            DataRequired(message="El nombre de la empresa es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    contacto = StringField(
        "Teléfono de contacto",
        validators=[
            DataRequired(message="El teléfono de contacto es obligatorio."),
            Length(
                min=10,
                max=15,
                message="El teléfono debe tener entre 10 y 15 caracteres."
            )
        ]
    )

    servicio = StringField(
        "Servicio proporcionado",
        validators=[
            DataRequired(message="El servicio es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El servicio debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    submit = SubmitField("Registrar proveedor")

