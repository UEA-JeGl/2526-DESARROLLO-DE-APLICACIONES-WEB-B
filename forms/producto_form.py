from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(message="El nombre del producto es obligatorio."),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Desarrollo Web", "Desarrollo Web"),
            ("Soporte Técnico", "Soporte Técnico"),
            ("Capacitación", "Capacitación"),
            ("Consultoría", "Consultoría")
        ],
        validators=[
            DataRequired(message="Debe seleccionar una categoría.")
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(message="El precio es obligatorio."),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(message="El stock es obligatorio."),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    submit = SubmitField("Registrar producto")
