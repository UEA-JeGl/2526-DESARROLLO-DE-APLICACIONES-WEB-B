from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm
import sqlite3
import os

# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)

# SECRET_KEY necesaria para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "TecnoSoluciones_2026_Semana11"

# Ruta de la base de datos SQLite
DATABASE = os.path.join("data", "ferreteria.db")


# ==========================================================
# CONEXIÓN CON SQLITE
# ==========================================================

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# INICIALIZAR BASE DE DATOS
# ==========================================================

def init_db():
    os.makedirs("data", exist_ok=True)

    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ==========================================================
# PÁGINA PRINCIPAL
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
# MÓDULO DE PRODUCTOS - SELECT
# ==========================================================

@app.route("/productos")
def productos():

    conn = get_db_connection()

    productos = conn.execute("""
        SELECT id, nombre, categoria, precio, stock
        FROM productos
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "productos.html",
        productos=productos
    )


# ==========================================================
# FORMULARIO DE PRODUCTOS - INSERT
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        conn = get_db_connection()

        conn.execute("""
            INSERT INTO productos (nombre, categoria, precio, stock)
            VALUES (?, ?, ?, ?)
        """, (
            form.nombre.data,
            form.categoria.data,
            float(form.precio.data),
            form.stock.data
        ))

        conn.commit()
        conn.close()

        flash(
            f"Producto '{form.nombre.data}' registrado correctamente.",
            "success"
        )

        return redirect(url_for("productos"))

    return render_template(
        "formulario_producto.html",
        form=form
    )


# ==========================================================
# MÓDULO DE CLIENTES
# ==========================================================

@app.route("/clientes")
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
# FORMULARIO DE CLIENTES
# ==========================================================

@app.route("/clientes/nuevo", methods=["GET", "POST"])
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
# MÓDULO DE PROVEEDORES
# ==========================================================

@app.route("/proveedores")
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
# FORMULARIO DE PROVEEDORES
# ==========================================================

@app.route("/proveedores/nuevo", methods=["GET", "POST"])
def formulario_proveedor():

    form = ProveedorForm()

    if form.validate_on_submit():

        proveedor = {
            "empresa": form.empresa.data,
            "contacto": form.contacto.data,
            "servicio": form.servicio.data
        }

        flash(
            f"Proveedor '{proveedor['empresa']} registrado correctamente.",
            "success"
        )

        return redirect(url_for("proveedores"))

    return render_template(
        "formulario_proveedor.html",
        form=form
    )


# ==========================================================
# MÓDULO DE FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
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
# FORMULARIO DE FACTURACIÓN
# ==========================================================

@app.route("/facturacion/nueva", methods=["GET", "POST"])
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
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    init_db()
    app.run(debug=True)