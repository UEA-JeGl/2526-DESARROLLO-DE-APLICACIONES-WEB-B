from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from psycopg2.extras import RealDictCursor

from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
from forms.usuario_form import UsuarioForm
from forms.login_form import LoginForm

from conexion.conexion import obtener_conexion
from models import Usuario


app = Flask("tecnosoluciones")

app.config["SECRET_KEY"] = "TecnoSoluciones_2026_Semana11"

csrf = CSRFProtect(app)


# ==========================================================
# CREAR TABLA CLIENTES AUTOMÁTICAMENTE
# ==========================================================

def crear_tabla_clientes():

    conexion = None

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                correo VARCHAR(150) NOT NULL,
                tipo VARCHAR(30) NOT NULL,
                estado VARCHAR(20) NOT NULL DEFAULT 'Activo'
            )
        """)

        conexion.commit()

        cursor.close()
        conexion.close()

        print("Tabla clientes verificada correctamente.")

    except Exception as e:

        print(
            "ERROR AL CREAR TABLA CLIENTES:",
            e
        )

        if conexion:
            conexion.close()


crear_tabla_clientes()

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


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
    """, (user_id,))

    datos = cursor.fetchone()

    cursor.close()
    conexion.close()

    if datos:
        return Usuario(
            datos["id"],
            datos["usuario"],
            datos["password"]
        )

    return None


# ==========================================================
# INICIO
# ==========================================================

@app.route("/")
def inicio():

    nombre_empresa = "TecnoSoluciones"

    informacion = {
        "titulo": "Servicios Tecnológicos",
        "descripcion": (
            "Soluciones tecnológicas para estudiantes, "
            "emprendedores y empresas."
        ),
        "anio": 2026
    }

    servicios = [
        {
            "nombre": "Desarrollo Web",
            "descripcion": (
                "Diseño y desarrollo de sitios web modernos "
                "y funcionales."
            )
        },
        {
            "nombre": "Soporte Técnico",
            "descripcion": (
                "Mantenimiento y asistencia para computadores "
                "y equipos."
            )
        },
        {
            "nombre": "Capacitación",
            "descripcion": (
                "Cursos sobre herramientas digitales y tecnología."
            )
        },
        {
            "nombre": "Consultoría",
            "descripcion": (
                "Asesoría para proyectos y soluciones tecnológicas."
            )
        }
    ]

    return render_template(
        "index.html",
        nombre_empresa=nombre_empresa,
        informacion=informacion,
        servicios=servicios
    )


# ==========================================================
# REGISTRO DE USUARIO
# ==========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    form = UsuarioForm()

    if form.validate_on_submit():

        usuario = form.usuario.data
        password = form.password.data

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT id
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        usuario_existente = cursor.fetchone()

        if usuario_existente:

            cursor.close()
            conexion.close()

            flash(
                "El nombre de usuario ya existe.",
                "danger"
            )

            return render_template(
                "registro.html",
                form=form
            )

        password_hash = generate_password_hash(password)

        cursor.close()

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
        """, (
            usuario,
            password_hash
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente. "
            "Ahora puede iniciar sesión.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "registro.html",
        form=form
    )


# ==========================================================
# LOGIN
# ==========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(
            url_for("dashboard")
        )

    form = LoginForm()

    if form.validate_on_submit():

        usuario = form.usuario.data
        password = form.password.data

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
        """, (usuario,))

        datos = cursor.fetchone()

        cursor.close()
        conexion.close()

        if datos and check_password_hash(
            datos["password"],
            password
        ):

            usuario_obj = Usuario(
                datos["id"],
                datos["usuario"],
                datos["password"]
            )

            login_user(usuario_obj)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Usuario o contraseña incorrectos.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
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
# FUNCIÓN PARA CARGAR PROVEEDORES
# ==========================================================

def cargar_proveedores(form):

    conexion = obtener_conexion()

    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_proveedor, nombre
        FROM proveedores
        ORDER BY nombre
    """)

    proveedores = cursor.fetchall()

    form.id_proveedor.choices = [
        (
            proveedor[0],
            proveedor[1]
        )
        for proveedor in proveedores
    ]

    cursor.close()
    conexion.close()


# ==========================================================
# PRODUCTOS - LEER
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

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

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================================
# PRODUCTOS - CREAR
# ==========================================================

@app.route(
    "/productos/nuevo",
    methods=["GET", "POST"]
)
@login_required
def formulario_producto():

    form = ProductoForm()

    cargar_proveedores(form)

    if form.validate_on_submit():

        conexion = obtener_conexion()

        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO productos
            (
                nombre,
                categoria,
                precio,
                stock,
                id_proveedor
            )
            VALUES
            (%s, %s, %s, %s, %s)
        """, (
            form.nombre.data,
            form.categoria.data,
            form.precio.data,
            form.stock.data,
            form.id_proveedor.data
        ))

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            f"Producto '{form.nombre.data}' "
            "registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("productos")
        )

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=False
    )


# ==========================================================
# PRODUCTOS - ACTUALIZAR
# ==========================================================

@app.route(
    "/productos/editar/<int:id_producto>",
    methods=["GET", "POST"]
)
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()

    cursor = conexion.cursor(
        cursor_factory=RealDictCursor
    )

    cursor.execute("""
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock,
            id_proveedor
        FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not producto:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(
            url_for("productos")
        )

    form = ProductoForm()

    cargar_proveedores(form)

    if form.validate_on_submit():

        conexion = obtener_conexion()

        cursor = conexion.cursor()

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

        cursor.close()
        conexion.close()

        flash(
            f"Producto '{form.nombre.data}' "
            "actualizado correctamente.",
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
        editar=True,
        id_producto=id_producto
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

    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM productos
        WHERE id_producto = %s
    """, (id_producto,))

    conexion.commit()

    filas_eliminadas = cursor.rowcount

    cursor.close()
    conexion.close()

    if filas_eliminadas > 0:

        flash(
            "Producto eliminado correctamente.",
            "success"
        )

    else:

        flash(
            "Producto no encontrado.",
            "danger"
        )

    return redirect(
        url_for("productos")
    )


# ==========================================================
# CLIENTES - LEER
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    conexion = None

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT
                id,
                nombre,
                correo,
                tipo,
                estado
            FROM clientes
            ORDER BY id DESC
        """)

        clientes = cursor.fetchall()

        cursor.close()
        conexion.close()

        return render_template(
            "clientes.html",
            clientes=clientes
        )

    except Exception as e:

        print(
            "ERROR AL CARGAR CLIENTES:",
            e
        )

        if conexion:
            conexion.close()

        flash(
            "No se pudieron cargar los clientes.",
            "danger"
        )

        return render_template(
            "clientes.html",
            clientes=[]
        )


# ==========================================================
# EDITAR CLIENTE
# ==========================================================

@app.route(
    "/clientes/editar/<int:id>",
    methods=["GET", "POST"]
)
@login_required
def editar_cliente(id):

    conexion = None

    try:

        conexion = obtener_conexion()

        cursor = conexion.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id,
                nombre,
                correo,
                tipo,
                estado
            FROM clientes
            WHERE id = %s
            """,
            (id,)
        )

        cliente = cursor.fetchone()

        cursor.close()
        conexion.close()

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

            conexion = obtener_conexion()

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE clientes
                SET
                    nombre = %s,
                    correo = %s,
                    tipo = %s,
                    estado = %s
                WHERE id = %s
                """,
                (
                    form.nombre.data,
                    form.correo.data,
                    form.tipo.data,
                    form.estado.data,
                    id
                )
            )

            conexion.commit()

            cursor.close()
            conexion.close()

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
            form.tipo.data = cliente["tipo"]
            form.estado.data = cliente["estado"]

        return render_template(
            "formulario_cliente.html",
            form=form,
            titulo="Editar cliente"
        )

    except Exception as e:

        print(
            "ERROR AL EDITAR CLIENTE:",
            e
        )

        if conexion:

            conexion.rollback()
            conexion.close()

        flash(
            "No se pudo actualizar el cliente.",
            "danger"
        )

        return redirect(
            url_for("clientes")
        )
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

        proveedor = {
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "servicio": form.servicio.data
        }

        flash(
            f"Proveedor '{proveedor['empresa']}' "
            "registrado correctamente.",
            "success"
        )

        return redirect(
            url_for("proveedores")
        )

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================================
# FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
@login_required
def facturacion():

    facturas_demo = [
        {
            "numero": "FAC-001",
            "cliente": "Juan Pérez",
            "fecha": "15/08/2026",
            "total": 350.00,
            "estado": "Pagada"
        },
        {
            "numero": "FAC-002",
            "cliente": "María López",
            "fecha": "16/08/2026",
            "total": 90.00,
            "estado": "Pendiente"
        },
        {
            "numero": "FAC-003",
            "cliente": "Carlos Andrade",
            "fecha": "16/08/2026",
            "total": 60.00,
            "estado": "Pagada"
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas_demo
    )


# ==========================================================
# FACTURACIÓN - NUEVA
# ==========================================================

@app.route(
    "/facturacion/nueva",
    methods=["GET", "POST"]
)
@login_required
def formulario_facturacion():

    form = FacturacionForm()

    if form.validate_on_submit():

        factura = {
            "numero": form.numero.data,
            "cliente": form.cliente.data,
            "fecha": form.fecha.data,
            "total": form.total.data
        }

        flash(
            f"Factura '{factura['numero']}' "
            "registrada correctamente.",
            "success"
        )

        return redirect(
            url_for("facturacion")
        )

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)