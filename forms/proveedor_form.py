from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email


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

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(message="El teléfono es obligatorio."),
            Length(
                min=10,
                max=15,
                message="El teléfono debe tener entre 10 y 15 caracteres."
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

    contacto = StringField(
        "Persona de contacto",
        validators=[
            DataRequired(message="La persona de contacto es obligatoria."),
            Length(
                min=3,
                max=100,
                message="El contacto debe tener entre 3 y 100 caracteres."
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

    estado = SelectField(
        "Estado",
        choices=[
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        default="Activo",
        validators=[
            DataRequired(message="Debe seleccionar un estado.")
        ]
    )

    submit = SubmitField("Guardar proveedor")