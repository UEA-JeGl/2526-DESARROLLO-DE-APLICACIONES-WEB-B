from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Length,
    NumberRange
)


class ProductoForm(FlaskForm):

    # ==========================================================
    # NOMBRE
    # ==========================================================

    nombre = StringField(
        "Nombre del producto",
        validators=[
            DataRequired(
                message="El nombre del producto es obligatorio."
            ),
            Length(
                min=3,
                max=100,
                message="El nombre debe tener entre 3 y 100 caracteres."
            )
        ]
    )


    # ==========================================================
    # CATEGORÍA
    # ==========================================================

    categoria = SelectField(
        "Categoría",
        choices=[
            ("", "Seleccione una categoría"),
            ("Desarrollo Web", "Desarrollo Web"),
            ("Soporte Técnico", "Soporte Técnico"),
            ("Capacitación", "Capacitación"),
            ("Consultoría", "Consultoría"),
            ("Herramientas", "Herramientas"),
            ("Accesorios", "Accesorios")
        ],
        validators=[
            DataRequired(
                message="Debe seleccionar una categoría."
            )
        ]
    )


    # ==========================================================
    # PRECIO
    # ==========================================================

    precio = DecimalField(
        "Precio",
        places=2,
        rounding=None,
        validators=[
            DataRequired(
                message="El precio es obligatorio."
            ),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor que 0."
            )
        ]
    )


    # ==========================================================
    # STOCK
    # ==========================================================

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(
                message="El stock es obligatorio."
            ),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )


    # ==========================================================
    # PROVEEDOR
    # ==========================================================

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired(
                message="Debe seleccionar un proveedor."
            )
        ]
    )


    # ==========================================================
    # BOTÓN
    # ==========================================================

    submit = SubmitField(
        "Guardar producto"
    )