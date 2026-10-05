import os

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm, CSRFProtect
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

from wtforms import (
    StringField,
    PasswordField,
    DecimalField,
    IntegerField,
    SelectField,
    DateField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange
)

import psycopg2
from psycopg2.extras import RealDictCursor


# ==========================================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================================

app = Flask("tecnosoluciones")

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "clave-secreta-tecnosoluciones-2026"
)

csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder."
login_manager.login_message_category = "warning"


# ==========================================================
# CONEXIÓN A POSTGRESQL
# ==========================================================

def obtener_conexion():

    database_url = os.environ.get("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="tecnosoluciones",
        user="postgres",
        password=os.environ.get(
            "POSTGRES_PASSWORD",
            "12345"
        )
    )


# ==========================================================
# USUARIO PARA FLASK-LOGIN
# ==========================================================

class Usuario(UserMixin):

    def __init__(self, id, usuario, password):

        self.id = id
        self.usuario = usuario
        self.password = password


@login_manager.user_loader
def cargar_usuario(user_id):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(cursor_factory=RealDictCursor) as cursor:

            cursor.execute(
                """
                SELECT id, usuario, password
                FROM usuarios
                WHERE id = %s
                """,
                (user_id,)
            )

            usuario = cursor.fetchone()

            if usuario:

                return Usuario(
                    usuario["id"],
                    usuario["usuario"],
                    usuario["password"]
                )

    except Exception as e:

        print(f"Error al cargar usuario: {e}")

    finally:

        conexion.close()

    return None


# ==========================================================
# FORMULARIOS
# ==========================================================

class LoginForm(FlaskForm):

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Iniciar sesión")


class RegistroForm(FlaskForm):

    nombre = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(min=6, max=100)
        ]
    )

    submit = SubmitField("Registrarse")


class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            ("Desarrollo Web", "Desarrollo Web"),
            ("Soporte Técnico", "Soporte Técnico"),
            ("Capacitación", "Capacitación"),
            ("Consultoría", "Consultoría")
        ],
        validators=[
            DataRequired()
        ]
    )

    precio = DecimalField(
        "Precio",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="El precio debe ser mayor a 0."
            )
        ],
        places=2
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(),
            NumberRange(
                min=0,
                message="El stock no puede ser negativo."
            )
        ]
    )

    id_proveedor = SelectField(
        "Proveedor",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Guardar")


class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(min=7, max=20)
        ]
    )

    submit = SubmitField("Guardar")


class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(min=7, max=20)
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email(),
            Length(max=120)
        ]
    )

    contacto = StringField(
        "Contacto",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    servicio = StringField(
        "Servicio",
        validators=[
            DataRequired(),
            Length(min=3, max=150)
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Activo", "Activo"),
            ("Inactivo", "Inactivo")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Guardar")


class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(),
            Length(min=3, max=30)
        ]
    )

    id_cliente = SelectField(
        "Cliente",
        coerce=int,
        validators=[
            DataRequired()
        ]
    )

    fecha = DateField(
        "Fecha",
        format="%Y-%m-%d",
        validators=[
            DataRequired()
        ]
    )

    total = DecimalField(
        "Total",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01,
                message="El total debe ser mayor a 0."
            )
        ],
        places=2
    )

    estado = SelectField(
        "Estado",
        choices=[
            ("Pendiente", "Pendiente"),
            ("Pagada", "Pagada"),
            ("Anulada", "Anulada")
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Guardar")


# ==========================================================
# CREAR / VERIFICAR TABLA CLIENTES
# ==========================================================

def crear_tabla_clientes():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(120) NOT NULL,
                    telefono VARCHAR(20) NOT NULL
                );
                """
            )

        conexion.commit()

        print("Tabla clientes verificada correctamente.")

    except Exception as e:

        conexion.rollback()

        print(
            f"Error al verificar tabla clientes: {e}"
        )

    finally:

        conexion.close()


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():

    informacion = {
        "titulo": "TecnoSoluciones",
        "descripcion": (
            "Servicios de desarrollo web, soporte técnico, "
            "capacitación y consultoría tecnológica."
        ),
        "empresa": "TecnoSoluciones",
        "anio": 2026
    }

    return render_template(
        "index.html",
        informacion=informacion
    )


# ==========================================================
# REGISTRO
# ==========================================================

@app.route(
    "/registro",
    methods=["GET", "POST"]
)
def registro():

    form = RegistroForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT id
                    FROM usuarios
                    WHERE usuario = %s
                    """,
                    (form.correo.data,)
                )

                existe = cursor.fetchone()

                if existe:

                    flash(
                        "El correo ya está registrado.",
                        "warning"
                    )

                    return render_template(
                        "registro.html",
                        form=form
                    )

                password_hash = generate_password_hash(
                    form.password.data
                )

                cursor.execute(
                    """
                    INSERT INTO usuarios
                    (usuario, password)
                    VALUES (%s, %s)
                    """,
                    (
                        form.correo.data,
                        password_hash
                    )
                )

            conexion.commit()

            flash(
                "Registro exitoso. Ahora puedes iniciar sesión.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except Exception as e:

            conexion.rollback()

            flash(
                f"Error al registrarse: {e}",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "registro.html",
        form=form
    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if current_user.is_authenticated:

        return redirect(
            url_for("dashboard")
        )

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute(
                    """
                    SELECT id, usuario, password
                    FROM usuarios
                    WHERE usuario = %s
                    """,
                    (form.correo.data,)
                )

                usuario = cursor.fetchone()

            if usuario and check_password_hash(
                usuario["password"],
                form.password.data
            ):

                usuario_obj = Usuario(
                    usuario["id"],
                    usuario["usuario"],
                    usuario["password"]
                )

                login_user(usuario_obj)

                flash(
                    "Inicio de sesión exitoso.",
                    "success"
                )

                return redirect(
                    url_for("dashboard")
                )

            flash(
                "Correo o contraseña incorrectos.",
                "danger"
            )

        except Exception as e:

            flash(
                f"Error al iniciar sesión: {e}",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "login.html",
        form=form
    )


# ==========================================================
# LOGOUT
# ==========================================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("login")
    )


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# ==========================================================
# PRODUCTOS - LISTAR
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    p.id_producto,
                    p.nombre,
                    p.categoria,
                    p.precio,
                    p.stock,
                    p.id_proveedor,
                    pr.nombre AS proveedor
                FROM productos p
                LEFT JOIN proveedores pr
                    ON p.id_proveedor = pr.id_proveedor
                ORDER BY p.id_producto DESC
                """
            )

            productos_lista = cursor.fetchall()

        return render_template(
            "productos.html",
            productos=productos_lista
        )

    except Exception as e:

        flash(
            f"Error al consultar productos: {e}",
            "danger"
        )

        return render_template(
            "productos.html",
            productos=[]
        )

    finally:

        conexion.close()


# ==========================================================
# PRODUCTOS - NUEVO
# ==========================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def formulario_producto():

    form = ProductoForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT id_proveedor, nombre
                FROM proveedores
                ORDER BY nombre
                """
            )

            proveedores_lista = cursor.fetchall()

        form.id_proveedor.choices = [
            (
                proveedor["id_proveedor"],
                proveedor["nombre"]
            )
            for proveedor in proveedores_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO productos
                    (
                        nombre,
                        categoria,
                        precio,
                        stock,
                        id_proveedor
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        form.nombre.data,
                        form.categoria.data,
                        form.precio.data,
                        form.stock.data,
                        form.id_proveedor.data
                    )
                )

            conexion.commit()

            flash(
                "Producto registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("productos")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al registrar producto: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Nuevo producto"
    )


# ==========================================================
# PRODUCTOS - EDITAR
# ==========================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    form = ProductoForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT id_proveedor, nombre
                FROM proveedores
                ORDER BY nombre
                """
            )

            proveedores_lista = cursor.fetchall()

            form.id_proveedor.choices = [
                (
                    proveedor["id_proveedor"],
                    proveedor["nombre"]
                )
                for proveedor in proveedores_lista
            ]

            cursor.execute(
                """
                SELECT
                    id_producto,
                    nombre,
                    categoria,
                    precio,
                    stock,
                    id_proveedor
                FROM productos
                WHERE id_producto = %s
                """,
                (id_producto,)
            )

            producto = cursor.fetchone()

        if not producto:

            flash(
                "Producto no encontrado.",
                "warning"
            )

            return redirect(
                url_for("productos")
            )

        if request.method == "GET":

            form.nombre.data = producto["nombre"]
            form.categoria.data = producto["categoria"]
            form.precio.data = producto["precio"]
            form.stock.data = producto["stock"]
            form.id_proveedor.data = producto["id_proveedor"]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE productos
                    SET
                        nombre = %s,
                        categoria = %s,
                        precio = %s,
                        stock = %s,
                        id_proveedor = %s
                    WHERE id_producto = %s
                    """,
                    (
                        form.nombre.data,
                        form.categoria.data,
                        form.precio.data,
                        form.stock.data,
                        form.id_proveedor.data,
                        id_producto
                    )
                )

            conexion.commit()

            flash(
                "Producto actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("productos")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar producto: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_producto.html",
        form=form,
        titulo="Editar producto"
    )


# ==========================================================
# PRODUCTOS - ELIMINAR
# ==========================================================

@app.route(
    "/productos/eliminar/<int:id_producto>",
    methods=["POST"]
)
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM productos
                WHERE id_producto = %s
                """,
                (id_producto,)
            )

        conexion.commit()

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al eliminar producto: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(
        url_for("productos")
    )


# ==========================================================
# CLIENTES - LISTAR
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    nombre,
                    correo,
                    telefono
                FROM clientes
                ORDER BY id DESC
                """
            )

            clientes_lista = cursor.fetchall()

        return render_template(
            "clientes.html",
            clientes=clientes_lista
        )

    except Exception as e:

        flash(
            f"Error al consultar clientes: {e}",
            "danger"
        )

        return render_template(
            "clientes.html",
            clientes=[]
        )

    finally:

        conexion.close()


# ==========================================================
# CLIENTES - NUEVO
# ==========================================================

@app.route(
    "/clientes/nuevo",
    methods=["GET", "POST"]
)
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO clientes
                    (
                        nombre,
                        correo,
                        telefono
                    )
                    VALUES (%s, %s, %s)
                    """,
                    (
                        form.nombre.data,
                        form.correo.data,
                        form.telefono.data
                    )
                )

            conexion.commit()

            flash(
                "Cliente registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("clientes")
            )

        except Exception as e:

            conexion.rollback()

            flash(
                f"Error al registrar cliente: {e}",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Nuevo cliente"
    )


# ==========================================================
# CLIENTES - EDITAR
# ==========================================================

@app.route(
    "/clientes/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id):

    form = ClienteForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    nombre,
                    correo,
                    telefono
                FROM clientes
                WHERE id = %s
                """,
                (id,)
            )

            cliente = cursor.fetchone()

        if not cliente:

            flash(
                "Cliente no encontrado.",
                "warning"
            )

            return redirect(
                url_for("clientes")
            )

        if request.method == "GET":

            form.nombre.data = cliente["nombre"]
            form.correo.data = cliente["correo"]
            form.telefono.data = cliente["telefono"]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE clientes
                    SET
                        nombre = %s,
                        correo = %s,
                        telefono = %s
                    WHERE id = %s
                    """,
                    (
                        form.nombre.data,
                        form.correo.data,
                        form.telefono.data,
                        id
                    )
                )

            conexion.commit()

            flash(
                "Cliente actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("clientes")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar cliente: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_cliente.html",
        form=form,
        titulo="Editar cliente"
    )


# ==========================================================
# CLIENTES - ELIMINAR
# ==========================================================

@app.route(
    "/clientes/eliminar/<int:id>",
    methods=["POST"]
)
@login_required
def eliminar_cliente(id):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM clientes
                WHERE id = %s
                """,
                (id,)
            )

        conexion.commit()

        flash(
            "Cliente eliminado correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al eliminar cliente: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(
        url_for("clientes")
    )


# ==========================================================
# PROVEEDORES - LISTAR
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id_proveedor,
                    nombre,
                    telefono,
                    correo,
                    contacto,
                    servicio,
                    estado
                FROM proveedores
                ORDER BY id_proveedor DESC
                """
            )

            proveedores_lista = cursor.fetchall()

        return render_template(
            "proveedores.html",
            proveedores=proveedores_lista
        )

    except Exception as e:

        flash(
            f"Error al consultar proveedores: {e}",
            "danger"
        )

        return render_template(
            "proveedores.html",
            proveedores=[]
        )

    finally:

        conexion.close()


# ==========================================================
# PROVEEDORES - NUEVO
# ==========================================================

@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
@login_required
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO proveedores
                    (
                        nombre,
                        telefono,
                        correo,
                        contacto,
                        servicio,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (
                        form.nombre.data,
                        form.telefono.data,
                        form.correo.data,
                        form.contacto.data,
                        form.servicio.data,
                        form.estado.data
                    )
                )

            conexion.commit()

            flash(
                "Proveedor registrado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

        except Exception as e:

            conexion.rollback()

            flash(
                f"Error al registrar proveedor: {e}",
                "danger"
            )

        finally:

            conexion.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Nuevo proveedor"
    )


# ==========================================================
# PROVEEDORES - EDITAR
# ==========================================================

@app.route(
    "/proveedores/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id_proveedor):

    form = ProveedorForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id_proveedor,
                    nombre,
                    telefono,
                    correo,
                    contacto,
                    servicio,
                    estado
                FROM proveedores
                WHERE id_proveedor = %s
                """,
                (id_proveedor,)
            )

            proveedor = cursor.fetchone()

        if not proveedor:

            flash(
                "Proveedor no encontrado.",
                "warning"
            )

            return redirect(
                url_for("proveedores")
            )

        if request.method == "GET":

            form.nombre.data = proveedor["nombre"]
            form.telefono.data = proveedor["telefono"]
            form.correo.data = proveedor["correo"]
            form.contacto.data = proveedor["contacto"]
            form.servicio.data = proveedor["servicio"]
            form.estado.data = proveedor["estado"]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE proveedores
                    SET
                        nombre = %s,
                        telefono = %s,
                        correo = %s,
                        contacto = %s,
                        servicio = %s,
                        estado = %s
                    WHERE id_proveedor = %s
                    """,
                    (
                        form.nombre.data,
                        form.telefono.data,
                        form.correo.data,
                        form.contacto.data,
                        form.servicio.data,
                        form.estado.data,
                        id_proveedor
                    )
                )

            conexion.commit()

            flash(
                "Proveedor actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar proveedor: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_proveedor.html",
        form=form,
        titulo="Editar proveedor"
    )


# ==========================================================
# PROVEEDORES - ELIMINAR
# ==========================================================

@app.route(
    "/proveedores/eliminar/<int:id_proveedor>",
    methods=["POST"]
)
@login_required
def eliminar_proveedor(id_proveedor):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM proveedores
                WHERE id_proveedor = %s
                """,
                (id_proveedor,)
            )

        conexion.commit()

        flash(
            "Proveedor eliminado correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al eliminar proveedor: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(
        url_for("proveedores")
    )


# ==========================================================
# FACTURACIÓN - LISTAR
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    f.id_factura,
                    f.numero,
                    f.id_cliente,
                    c.nombre AS cliente,
                    f.fecha,
                    f.total,
                    f.estado
                FROM facturas f
                INNER JOIN clientes c
                    ON f.id_cliente = c.id
                ORDER BY f.id_factura DESC
                """
            )

            facturas_lista = cursor.fetchall()

        return render_template(
            "facturacion.html",
            facturas=facturas_lista
        )

    except Exception as e:

        flash(
            f"Error al consultar facturación: {e}",
            "danger"
        )

        return render_template(
            "facturacion.html",
            facturas=[]
        )

    finally:

        conexion.close()


# ==========================================================
# FACTURACIÓN - NUEVA
# ==========================================================

@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
@login_required
def nueva_factura():

    form = FacturacionForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    nombre
                FROM clientes
                ORDER BY nombre
                """
            )

            clientes_lista = cursor.fetchall()

        form.id_cliente.choices = [
            (
                cliente["id"],
                cliente["nombre"]
            )
            for cliente in clientes_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    INSERT INTO facturas
                    (
                        numero,
                        id_cliente,
                        fecha,
                        total,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        form.numero.data,
                        form.id_cliente.data,
                        form.fecha.data,
                        form.total.data,
                        form.estado.data
                    )
                )

            conexion.commit()

            flash(
                "Factura registrada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al registrar factura: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Nueva factura"
    )


# ==========================================================
# FACTURACIÓN - EDITAR
# ==========================================================

@app.route(
    "/facturacion/editar/<int:id_factura>",
    methods=["GET", "POST"]
)
@login_required
def editar_factura(id_factura):

    form = FacturacionForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute(
                """
                SELECT
                    id,
                    nombre
                FROM clientes
                ORDER BY nombre
                """
            )

            clientes_lista = cursor.fetchall()

            form.id_cliente.choices = [
                (
                    cliente["id"],
                    cliente["nombre"]
                )
                for cliente in clientes_lista
            ]

            cursor.execute(
                """
                SELECT
                    id_factura,
                    numero,
                    id_cliente,
                    fecha,
                    total,
                    estado
                FROM facturas
                WHERE id_factura = %s
                """,
                (id_factura,)
            )

            factura = cursor.fetchone()

        if not factura:

            flash(
                "Factura no encontrada.",
                "warning"
            )

            return redirect(
                url_for("facturacion")
            )

        if request.method == "GET":

            form.numero.data = factura["numero"]
            form.id_cliente.data = factura["id_cliente"]
            form.fecha.data = factura["fecha"]
            form.total.data = factura["total"]
            form.estado.data = factura["estado"]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute(
                    """
                    UPDATE facturas
                    SET
                        numero = %s,
                        id_cliente = %s,
                        fecha = %s,
                        total = %s,
                        estado = %s
                    WHERE id_factura = %s
                    """,
                    (
                        form.numero.data,
                        form.id_cliente.data,
                        form.fecha.data,
                        form.total.data,
                        form.estado.data,
                        id_factura
                    )
                )

            conexion.commit()

            flash(
                "Factura actualizada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar factura: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return render_template(
        "formulario_facturacion.html",
        form=form,
        titulo="Editar factura"
    )


# ==========================================================
# FACTURACIÓN - ELIMINAR
# ==========================================================

@app.route(
    "/facturacion/eliminar/<int:id_factura>",
    methods=["POST"]
)
@login_required
def eliminar_factura(id_factura):

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute(
                """
                DELETE FROM facturas
                WHERE id_factura = %s
                """,
                (id_factura,)
            )

        conexion.commit()

        flash(
            "Factura eliminada correctamente.",
            "success"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al eliminar factura: {e}",
            "danger"
        )

    finally:

        conexion.close()

    return redirect(
        url_for("facturacion")
    )


# ==========================================================
# INICIAR APLICACIÓN
# ==========================================================

with app.app_context():

    crear_tabla_clientes()


if __name__ == "__main__":

    app.run(
        debug=True
    )