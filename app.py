from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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
# FLASK-LOGIN
# ==========================================================

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"
login_manager.login_message = "Debe iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT id, usuario, password
        FROM usuarios
        WHERE id = %s
        """,
        (user_id,)
    )

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
# PAGINA PRINCIPAL
# ==========================================================

@app.route("/")
def inicio():

    nombre_empresa = "TecnoSoluciones"

    informacion = {
        "titulo": "Servicios Tecnológicos",
        "descripcion": "Soluciones tecnológicas para estudiantes, emprendedores y empresas.",
        "anio": 2026
    }

    servicios = [
        {
            "nombre": "Desarrollo Web",
            "descripcion": "Diseño y desarrollo de sitios web modernos y funcionales."
        },
        {
            "nombre": "Soporte Técnico",
            "descripcion": "Mantenimiento y asistencia para computadores y equipos."
        },
        {
            "nombre": "Capacitación",
            "descripcion": "Cursos sobre herramientas digitales y tecnología."
        },
        {
            "nombre": "Consultoría",
            "descripcion": "Asesoría para proyectos y soluciones tecnológicas."
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
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

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

        cursor.execute(
            """
            INSERT INTO usuarios (usuario, password)
            VALUES (%s, %s)
            """,
            (usuario, password_hash)
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            "Usuario registrado correctamente. Ahora puede iniciar sesión.",
            "success"
        )

        return redirect(url_for("login"))

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
        return redirect(url_for("dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        usuario = form.usuario.data
        password = form.password.data

        conexion = obtener_conexion()
        cursor = conexion.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT id, usuario, password
            FROM usuarios
            WHERE usuario = %s
            """,
            (usuario,)
        )

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

            return redirect(url_for("dashboard"))

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

    return redirect(url_for("login"))


# ==========================================================
# PRODUCTOS
# ==========================================================

@app.route("/productos")
@login_required
def productos():

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

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

    productos = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================================
# NUEVO PRODUCTO
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            INSERT INTO productos
                (nombre, categoria, precio, stock)
            VALUES
                (%s, %s, %s, %s)
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            f"Producto '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=False
    )


# ==========================================================
# EDITAR PRODUCTO
# ==========================================================

@app.route("/productos/editar/<int:id_producto>", methods=["GET", "POST"])
@login_required
def editar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            id_producto,
            nombre,
            categoria,
            precio,
            stock
        FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

    producto = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not producto:

        flash(
            "Producto no encontrado.",
            "danger"
        )

        return redirect(url_for("productos"))

    form = ProductoForm()

    if form.validate_on_submit():

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        cursor.execute(
            """
            UPDATE productos
            SET
                nombre = %s,
                categoria = %s,
                precio = %s,
                stock = %s
            WHERE id_producto = %s
            """,
            (
                form.nombre.data,
                form.categoria.data,
                form.precio.data,
                form.stock.data,
                id_producto
            )
        )

        conexion.commit()

        cursor.close()
        conexion.close()

        flash(
            f"Producto '{form.nombre.data}' actualizado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    if not form.is_submitted():

        form.nombre.data = producto["nombre"]
        form.categoria.data = producto["categoria"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]

    return render_template(
        "formulario_producto.html",
        form=form,
        editar=True,
        id_producto=id_producto
    )


# ==========================================================
# ELIMINAR PRODUCTO
# ==========================================================

@app.route("/productos/eliminar/<int:id_producto>", methods=["POST"])
@login_required
def eliminar_producto(id_producto):

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        """
        DELETE FROM productos
        WHERE id_producto = %s
        """,
        (id_producto,)
    )

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

    return redirect(url_for("productos"))


# ==========================================================
# CLIENTES
# ==========================================================

@app.route("/clientes")
@login_required
def clientes():

    clientes_demo = [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "correo": "juan@gmail.com",
            "tipo": "Estudiante",
            "estado": "Activo"
        },
        {
            "id": 2,
            "nombre": "María López",
            "correo": "maria@gmail.com",
            "tipo": "Emprendedor",
            "estado": "Activo"
        },
        {
            "id": 3,
            "nombre": "Carlos Andrade",
            "correo": "carlos@gmail.com",
            "tipo": "Empresa",
            "estado": "Inactivo"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes_demo
    )


# ==========================================================
# NUEVO CLIENTE
# ==========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
@login_required
def formulario_cliente():

    form = ClienteForm()

    if form.validate_on_submit():

        cliente = {
            "nombre": form.nombre.data,
            "correo": form.correo.data,
            "tipo": form.tipo.data
        }

        flash(
            f"Cliente '{cliente['nombre']}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("clientes"))

    return render_template(
        "formulario_cliente.html",
        form=form
    )


# ==========================================================
# PROVEEDORES
# ==========================================================

@app.route("/proveedores")
@login_required
def proveedores():

    proveedores_demo = [
        {
            "empresa": "Tech Ecuador",
            "contacto": "0999999999",
            "servicio": "Equipos informáticos",
            "estado": "Activo"
        },
        {
            "empresa": "Digital Solutions",
            "contacto": "0988888888",
            "servicio": "Software",
            "estado": "Activo"
        },
        {
            "empresa": "InnovaTech",
            "contacto": "0977777777",
            "servicio": "Servicios tecnológicos",
            "estado": "Inactivo"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores_demo
    )


# ==========================================================
# NUEVO PROVEEDOR
# ==========================================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
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
            f"Proveedor '{proveedor['empresa']}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================================
# FACTURACION
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
# NUEVA FACTURA
# ==========================================================

@app.route("/facturacion/nueva", methods=["GET", "POST"])
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
            f"Factura '{factura['numero']}' registrada correctamente.",
            "success"
        )

        return redirect(url_for("facturacion"))

    return render_template(
        "formulario_facturacion.html",
        form=form
    )


# ==========================================================
# EJECUTAR APLICACION
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)