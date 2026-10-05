# ==========================================================
# TECNOSOLUCIONES
# SEMANA 15 - PROYECTO INTEGRADOR
# CRUD + LOGIN + REGISTRO + POSTGRESQL
# ==========================================================

from flask import Flask, render_template, redirect, url_for, flash

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user
)

from wtforms import (
    StringField,
    PasswordField,
    DecimalField,
    IntegerField,
    SelectField,
    SubmitField,
    DateField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    NumberRange
)

import psycopg2
import os

from psycopg2.extras import RealDictCursor


# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask("tecnosoluciones")

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "tecnosoluciones-clave-secreta"
)

csrf = CSRFProtect(app)


# ==========================================================
# CONFIGURACIÓN DE LOGIN
# ==========================================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"

login_manager.login_message = (
    "Debe iniciar sesión para acceder a esta página."
)

login_manager.login_message_category = "warning"


# ==========================================================
# CONEXIÓN A POSTGRESQL
# ==========================================================

def obtener_conexion():

    database_url = os.environ.get("DATABASE_URL")

    if database_url:

        return psycopg2.connect(
            database_url,
            sslmode="require"
        )

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
# MODELO USUARIO
# TABLA REAL:
# id | usuario | password
# ==========================================================

class Usuario:

    def __init__(
        self,
        id,
        usuario,
        password
    ):

        self.id = id
        self.usuario = usuario
        self.password = password

    @property
    def is_authenticated(self):

        return True

    @property
    def is_active(self):

        return True

    @property
    def is_anonymous(self):

        return False

    def get_id(self):

        return str(self.id)


# ==========================================================
# CARGAR USUARIO
# ==========================================================

@login_manager.user_loader
def cargar_usuario(usuario_id):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT
                    id,
                    usuario,
                    password
                FROM usuarios
                WHERE id = %s
            """, (usuario_id,))

            usuario = cursor.fetchone()

            if usuario:

                return Usuario(
                    usuario["id"],
                    usuario["usuario"],
                    usuario["password"]
                )

    except Exception as e:

        print(
            f"Error al cargar usuario: {e}"
        )

    finally:

        conexion.close()

    return None


# ==========================================================
# FORMULARIO LOGIN
# ==========================================================

class LoginForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Iniciar sesión"
    )


# ==========================================================
# FORMULARIO REGISTRO
# ==========================================================

class RegistroForm(FlaskForm):

    usuario = StringField(
        "Usuario",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=50
            )
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=100
            )
        ]
    )

    confirmar_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Registrarse"
    )


# ==========================================================
# FORMULARIO PRODUCTO
# ==========================================================

class ProductoForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100
            )
        ]
    )

    categoria = SelectField(
        "Categoría",
        choices=[
            (
                "Desarrollo Web",
                "Desarrollo Web"
            ),
            (
                "Soporte Técnico",
                "Soporte Técnico"
            ),
            (
                "Capacitación",
                "Capacitación"
            ),
            (
                "Consultoría",
                "Consultoría"
            )
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
                min=0.01
            )
        ],
        places=2
    )

    stock = IntegerField(
        "Stock",
        validators=[
            DataRequired(),
            NumberRange(
                min=0
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

    submit = SubmitField(
        "Guardar"
    )


# ==========================================================
# FORMULARIO CLIENTE
# ==========================================================

class ClienteForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100
            )
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(
                min=7,
                max=20
            )
        ]
    )

    submit = SubmitField(
        "Guardar"
    )


# ==========================================================
# FORMULARIO PROVEEDOR
# ==========================================================

class ProveedorForm(FlaskForm):

    nombre = StringField(
        "Nombre",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100
            )
        ]
    )

    telefono = StringField(
        "Teléfono",
        validators=[
            DataRequired(),
            Length(
                min=7,
                max=20
            )
        ]
    )

    correo = StringField(
        "Correo",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    contacto = StringField(
        "Contacto",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=100
            )
        ]
    )

    servicio = StringField(
        "Servicio",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=150
            )
        ]
    )

    estado = SelectField(
        "Estado",
        choices=[
            (
                "Activo",
                "Activo"
            ),
            (
                "Inactivo",
                "Inactivo"
            )
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Guardar"
    )


# ==========================================================
# FORMULARIO FACTURACIÓN
# ==========================================================

class FacturacionForm(FlaskForm):

    numero = StringField(
        "Número de factura",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=30
            )
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
        validators=[
            DataRequired()
        ],
        format="%Y-%m-%d"
    )

    total = DecimalField(
        "Total",
        validators=[
            DataRequired(),
            NumberRange(
                min=0.01
            )
        ],
        places=2
    )

    estado = SelectField(
        "Estado",
        choices=[
            (
                "Pendiente",
                "Pendiente"
            ),
            (
                "Pagada",
                "Pagada"
            ),
            (
                "Anulada",
                "Anulada"
            )
        ],
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField(
        "Guardar"
    )


# ==========================================================
# CREAR / ACTUALIZAR TABLA CLIENTES
# ==========================================================

def crear_tabla_clientes():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    correo VARCHAR(120) NOT NULL,
                    telefono VARCHAR(20)
                );
            """)

            cursor.execute("""
                ALTER TABLE clientes
                ADD COLUMN IF NOT EXISTS telefono VARCHAR(20);
            """)

            cursor.execute("""
                ALTER TABLE clientes
                DROP COLUMN IF EXISTS tipo;
            """)

            cursor.execute("""
                ALTER TABLE clientes
                DROP COLUMN IF EXISTS estado;
            """)

            cursor.execute("""
                UPDATE clientes
                SET telefono = '0000000000'
                WHERE telefono IS NULL;
            """)

            cursor.execute("""
                ALTER TABLE clientes
                ALTER COLUMN telefono SET NOT NULL;
            """)

        conexion.commit()

        print(
            "Tabla clientes verificada y actualizada correctamente."
        )

    except Exception as e:

        conexion.rollback()

        print(
            f"Error al verificar tabla clientes: {e}"
        )

    finally:

        conexion.close()


# ==========================================================
# CREAR / ACTUALIZAR TABLA PROVEEDORES
# ==========================================================

def crear_tabla_proveedores():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS proveedores (
                    id_proveedor SERIAL PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(20),
                    correo VARCHAR(120),
                    contacto VARCHAR(100),
                    servicio VARCHAR(150),
                    estado VARCHAR(20)
                );
            """)

            cursor.execute("""
                ALTER TABLE proveedores
                ADD COLUMN IF NOT EXISTS telefono VARCHAR(20);
            """)

            cursor.execute("""
                ALTER TABLE proveedores
                ADD COLUMN IF NOT EXISTS correo VARCHAR(120);
            """)

            cursor.execute("""
                ALTER TABLE proveedores
                ADD COLUMN IF NOT EXISTS contacto VARCHAR(100);
            """)

            cursor.execute("""
                ALTER TABLE proveedores
                ADD COLUMN IF NOT EXISTS servicio VARCHAR(150);
            """)

            cursor.execute("""
                ALTER TABLE proveedores
                ADD COLUMN IF NOT EXISTS estado VARCHAR(20);
            """)

            cursor.execute("""
                UPDATE proveedores
                SET contacto = 'Contacto pendiente'
                WHERE contacto IS NULL;
            """)

            cursor.execute("""
                UPDATE proveedores
                SET servicio = 'Servicio pendiente'
                WHERE servicio IS NULL;
            """)

            cursor.execute("""
                UPDATE proveedores
                SET estado = 'Activo'
                WHERE estado IS NULL;
            """)

        conexion.commit()

        print(
            "Tabla proveedores verificada y actualizada correctamente."
        )

    except Exception as e:

        conexion.rollback()

        print(
            f"Error al verificar tabla proveedores: {e}"
        )

    finally:

        conexion.close()


# ==========================================================
# CREAR / ACTUALIZAR TABLA FACTURAS
# ==========================================================

def crear_tabla_facturas():

    conexion = obtener_conexion()

    try:

        with conexion.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS facturas (
                    id_factura SERIAL PRIMARY KEY,
                    numero VARCHAR(30) NOT NULL,
                    id_cliente INTEGER NOT NULL,
                    fecha DATE NOT NULL,
                    total NUMERIC(10,2) NOT NULL,
                    estado VARCHAR(20) NOT NULL
                );
            """)

            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN IF NOT EXISTS numero VARCHAR(30);
            """)

            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN IF NOT EXISTS id_cliente INTEGER;
            """)

            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN IF NOT EXISTS fecha DATE;
            """)

            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN IF NOT EXISTS total NUMERIC(10,2);
            """)

            cursor.execute("""
                ALTER TABLE facturas
                ADD COLUMN IF NOT EXISTS estado VARCHAR(20);
            """)

            cursor.execute("""
                UPDATE facturas
                SET numero = 'FACT-PENDIENTE'
                WHERE numero IS NULL;
            """)

            cursor.execute("""
                UPDATE facturas
                SET fecha = CURRENT_DATE
                WHERE fecha IS NULL;
            """)

            cursor.execute("""
                UPDATE facturas
                SET total = 0.01
                WHERE total IS NULL;
            """)

            cursor.execute("""
                UPDATE facturas
                SET estado = 'Pendiente'
                WHERE estado IS NULL;
            """)

        conexion.commit()

        print(
            "Tabla facturas verificada y actualizada correctamente."
        )

    except Exception as e:

        conexion.rollback()

        print(
            f"Error al verificar tabla facturas: {e}"
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
        "descripcion":
            "Servicios de desarrollo web, soporte técnico, capacitación y consultoría tecnológica.",
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

        if (
            form.password.data
            != form.confirmar_password.data
        ):

            flash(
                "Las contraseñas no coinciden.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        conexion = obtener_conexion()

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
                    SELECT id
                    FROM usuarios
                    WHERE usuario = %s
                """, (
                    form.usuario.data,
                ))

                usuario_existente = cursor.fetchone()

                if usuario_existente:

                    flash(
                        "El usuario ya existe.",
                        "warning"
                    )

                    return render_template(
                        "registro.html",
                        form=form
                    )

                cursor.execute("""
                    INSERT INTO usuarios
                    (
                        usuario,
                        password
                    )
                    VALUES (%s, %s)
                """, (
                    form.usuario.data,
                    form.password.data
                ))

            conexion.commit()

            flash(
                "Usuario registrado correctamente. Ahora puede iniciar sesión.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except Exception as e:

            conexion.rollback()

            flash(
                f"Error al registrar usuario: {e}",
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

    form = LoginForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor(
                cursor_factory=RealDictCursor
            ) as cursor:

                cursor.execute("""
                    SELECT
                        id,
                        usuario,
                        password
                    FROM usuarios
                    WHERE usuario = %s
                """, (
                    form.usuario.data,
                ))

                usuario = cursor.fetchone()

            if usuario:

                if (
                    usuario["password"]
                    == form.password.data
                ):

                    usuario_obj = Usuario(
                        usuario["id"],
                        usuario["usuario"],
                        usuario["password"]
                    )

                    login_user(
                        usuario_obj
                    )

                    flash(
                        "Inicio de sesión exitoso.",
                        "success"
                    )

                    return redirect(
                        url_for("dashboard")
                    )

                else:

                    flash(
                        "Contraseña incorrecta.",
                        "danger"
                    )

            else:

                flash(
                    "Usuario no encontrado.",
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
# PRODUCTOS
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
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
            """)

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
# NUEVO PRODUCTO
# ==========================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_producto():

    form = ProductoForm()

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT
                    id_proveedor,
                    nombre
                FROM proveedores
                ORDER BY nombre
            """)

            proveedores_lista = cursor.fetchall()

        form.id_proveedor.choices = [
            (
                p["id_proveedor"],
                p["nombre"]
            )
            for p in proveedores_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO productos
                    (
                        nombre,
                        categoria,
                        precio,
                        stock,
                        id_proveedor
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    form.nombre.data,
                    form.categoria.data,
                    form.precio.data,
                    form.stock.data,
                    form.id_proveedor.data
                ))

            conexion.commit()

            flash(
                "Producto creado correctamente.",
                "success"
            )

            return redirect(
                url_for("productos")
            )

        return render_template(
            "formulario_producto.html",
            form=form,
            titulo="Nuevo producto"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al crear producto: {e}",
            "danger"
        )

        return render_template(
            "formulario_producto.html",
            form=form,
            titulo="Nuevo producto"
        )

    finally:

        conexion.close()


# ==========================================================
# EDITAR PRODUCTO
# ==========================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT *
                FROM productos
                WHERE id_producto = %s
            """, (
                id_producto,
            ))

            producto = cursor.fetchone()

            cursor.execute("""
                SELECT
                    id_proveedor,
                    nombre
                FROM proveedores
                ORDER BY nombre
            """)

            proveedores_lista = cursor.fetchall()

        if not producto:

            flash(
                "Producto no encontrado.",
                "danger"
            )

            return redirect(
                url_for("productos")
            )

        form = ProductoForm()

        form.id_proveedor.choices = [
            (
                p["id_proveedor"],
                p["nombre"]
            )
            for p in proveedores_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE productos
                    SET
                        nombre = %s,
                        categoria = %s,
                        precio = %s,
                        stock = %s,
                        id_proveedor = %s
                    WHERE id_producto = %s
                """, (
                    form.nombre.data,
                    form.categoria.data,
                    form.precio.data,
                    form.stock.data,
                    form.id_proveedor.data,
                    id_producto
                ))

            conexion.commit()

            flash(
                "Producto actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("productos")
            )

        if not form.is_submitted():

            form.nombre.data = producto["nombre"]
            form.categoria.data = producto["categoria"]
            form.precio.data = producto["precio"]
            form.stock.data = producto["stock"]
            form.id_proveedor.data = producto["id_proveedor"]

        return render_template(
            "formulario_producto.html",
            form=form,
            titulo="Editar producto"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar producto: {e}",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    finally:

        conexion.close()


# ==========================================================
# ELIMINAR PRODUCTO
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

            cursor.execute("""
                DELETE FROM productos
                WHERE id_producto = %s
            """, (
                id_producto,
            ))

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
# CLIENTES
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT
                    id,
                    nombre,
                    correo,
                    telefono
                FROM clientes
                ORDER BY id DESC
            """)

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
# NUEVO CLIENTE
# ==========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()

    if form.validate_on_submit():
        conexion = obtener_conexion()

        try:
            with conexion.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO clientes
                    (nombre, correo, telefono)
                    VALUES (%s, %s, %s)
                """, (
                    form.nombre.data,
                    form.correo.data,
                    form.telefono.data
                ))

            conexion.commit()
            flash("Cliente registrado correctamente.", "success")
            return redirect(url_for("clientes"))

        except Exception as e:
            conexion.rollback()
            flash(f"Error al registrar cliente: {e}", "danger")

        finally:
            conexion.close()

    return render_template("formulario_cliente.html", form=form)


# ==========================================================
# EDITAR CLIENTE
# ==========================================================


@app.route(
    "/clientes/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT
                    id,
                    nombre,
                    correo,
                    telefono
                FROM clientes
                WHERE id = %s
            """, (
                id,
            ))

            cliente = cursor.fetchone()

        if not cliente:

            flash(
                "Cliente no encontrado.",
                "danger"
            )

            return redirect(
                url_for("clientes")
            )

        form = ClienteForm()

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE clientes
                    SET
                        nombre = %s,
                        correo = %s,
                        telefono = %s
                    WHERE id = %s
                """, (
                    form.nombre.data,
                    form.correo.data,
                    form.telefono.data,
                    id
                ))

            conexion.commit()

            flash(
                "Cliente actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("clientes")
            )

        if not form.is_submitted():

            form.nombre.data = cliente["nombre"]
            form.correo.data = cliente["correo"]
            form.telefono.data = cliente["telefono"]

        return render_template(
            "formulario_cliente.html",
            form=form,
            titulo="Editar cliente"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar cliente: {e}",
            "danger"
        )

        return redirect(
            url_for("clientes")
        )

    finally:

        conexion.close()

# ==========================================================
# ELIMINAR CLIENTE
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

            cursor.execute("""
                DELETE FROM clientes
                WHERE id = %s
            """, (
                id,
            ))

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
# PROVEEDORES
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
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
            """)

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
# NUEVO PROVEEDOR
# ==========================================================

@app.route(
    "/proveedores/nuevo",
    methods=["GET", "POST"]
)
@login_required
def nuevo_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()

        try:

            with conexion.cursor() as cursor:

                cursor.execute("""
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
                """, (
                    form.nombre.data,
                    form.telefono.data,
                    form.correo.data,
                    form.contacto.data,
                    form.servicio.data,
                    form.estado.data
                ))

            conexion.commit()

            flash(
                "Proveedor creado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

        except Exception as e:

            conexion.rollback()

            flash(
                f"Error al crear proveedor: {e}",
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
# EDITAR PROVEEDOR
# ==========================================================

@app.route(
    "/proveedores/editar/<int:id_proveedor>",
    methods=["GET", "POST"]
)
@login_required
def editar_proveedor(id_proveedor):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
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
            """, (
                id_proveedor,
            ))

            proveedor = cursor.fetchone()

        if not proveedor:

            flash(
                "Proveedor no encontrado.",
                "danger"
            )

            return redirect(
                url_for("proveedores")
            )

        form = ProveedorForm()

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE proveedores
                    SET
                        nombre = %s,
                        telefono = %s,
                        correo = %s,
                        contacto = %s,
                        servicio = %s,
                        estado = %s
                    WHERE id_proveedor = %s
                """, (
                    form.nombre.data,
                    form.telefono.data,
                    form.correo.data,
                    form.contacto.data,
                    form.servicio.data,
                    form.estado.data,
                    id_proveedor
                ))

            conexion.commit()

            flash(
                "Proveedor actualizado correctamente.",
                "success"
            )

            return redirect(
                url_for("proveedores")
            )

        if not form.is_submitted():

            form.nombre.data = proveedor["nombre"]
            form.telefono.data = proveedor["telefono"]
            form.correo.data = proveedor["correo"]
            form.contacto.data = proveedor["contacto"]
            form.servicio.data = proveedor["servicio"]
            form.estado.data = proveedor["estado"]

        return render_template(
            "formulario_proveedor.html",
            form=form,
            titulo="Editar proveedor"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar proveedor: {e}",
            "danger"
        )

        return redirect(
            url_for("proveedores")
        )

    finally:

        conexion.close()


# ==========================================================
# ELIMINAR PROVEEDOR
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

            cursor.execute("""
                DELETE FROM proveedores
                WHERE id_proveedor = %s
            """, (
                id_proveedor,
            ))

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
# FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
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
            """)

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
# NUEVA FACTURA
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

            cursor.execute("""
                SELECT
                    id,
                    nombre
                FROM clientes
                ORDER BY nombre
            """)

            clientes_lista = cursor.fetchall()

        form.id_cliente.choices = [
            (
                c["id"],
                c["nombre"]
            )
            for c in clientes_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    INSERT INTO facturas
                    (
                        numero,
                        id_cliente,
                        fecha,
                        total,
                        estado
                    )
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    form.numero.data,
                    form.id_cliente.data,
                    form.fecha.data,
                    form.total.data,
                    form.estado.data
                ))

            conexion.commit()

            flash(
                "Factura creada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

        return render_template(
            "formulario_facturacion.html",
            form=form,
            titulo="Nueva factura"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al crear factura: {e}",
            "danger"
        )

        return render_template(
            "formulario_facturacion.html",
            form=form,
            titulo="Nueva factura"
        )

    finally:

        conexion.close()


# ==========================================================
# EDITAR FACTURA
# ==========================================================

@app.route(
    "/facturacion/editar/<int:id_factura>",
    methods=["GET", "POST"]
)
@login_required
def editar_factura(id_factura):

    conexion = obtener_conexion()

    try:

        with conexion.cursor(
            cursor_factory=RealDictCursor
        ) as cursor:

            cursor.execute("""
                SELECT
                    id_factura,
                    numero,
                    id_cliente,
                    fecha,
                    total,
                    estado
                FROM facturas
                WHERE id_factura = %s
            """, (
                id_factura,
            ))

            factura = cursor.fetchone()

            cursor.execute("""
                SELECT
                    id,
                    nombre
                FROM clientes
                ORDER BY nombre
            """)

            clientes_lista = cursor.fetchall()

        if not factura:

            flash(
                "Factura no encontrada.",
                "danger"
            )

            return redirect(
                url_for("facturacion")
            )

        form = FacturacionForm()

        form.id_cliente.choices = [
            (
                c["id"],
                c["nombre"]
            )
            for c in clientes_lista
        ]

        if form.validate_on_submit():

            with conexion.cursor() as cursor:

                cursor.execute("""
                    UPDATE facturas
                    SET
                        numero = %s,
                        id_cliente = %s,
                        fecha = %s,
                        total = %s,
                        estado = %s
                    WHERE id_factura = %s
                """, (
                    form.numero.data,
                    form.id_cliente.data,
                    form.fecha.data,
                    form.total.data,
                    form.estado.data,
                    id_factura
                ))

            conexion.commit()

            flash(
                "Factura actualizada correctamente.",
                "success"
            )

            return redirect(
                url_for("facturacion")
            )

        if not form.is_submitted():

            form.numero.data = factura["numero"]
            form.id_cliente.data = factura["id_cliente"]
            form.fecha.data = factura["fecha"]
            form.total.data = factura["total"]
            form.estado.data = factura["estado"]

        return render_template(
            "facturacion_form.html",
            form=form,
            titulo="Editar factura"
        )

    except Exception as e:

        conexion.rollback()

        flash(
            f"Error al editar factura: {e}",
            "danger"
        )

        return redirect(
            url_for("facturacion")
        )

    finally:

        conexion.close()


# ==========================================================
# ELIMINAR FACTURA
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

            cursor.execute("""
                DELETE FROM facturas
                WHERE id_factura = %s
            """, (
                id_factura,
            ))

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
# INICIALIZACIÓN
# ==========================================================

with app.app_context():

    crear_tabla_clientes()
    crear_tabla_proveedores()
    crear_tabla_facturas()


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )