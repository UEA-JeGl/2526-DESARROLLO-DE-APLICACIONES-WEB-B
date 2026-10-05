from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    DateField,
    DecimalField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(
                message="El número de factura es obligatorio."
            ),
            Length(
                min=3,
                max=30,
                message="El número debe tener entre 3 y 30 caracteres."
            )
        ]
    )

    id_cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un cliente."
            )
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired(
                message="La fecha es obligatoria."
            )
        ]
    )

    total = DecimalField(
        "Total",
        places=2,
        validators=[
            DataRequired(
                message="El total es obligatorio."
            ),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor que 0."
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Pagada", "Pagada"),
            ("Anulada", "Anulada")
        ],
        default="Pendiente",
        validators=[
            DataRequired(
                message="Debe seleccionar un estado."
            )
        ]
    )

    submit = SubmitField("Guardar factura")