from flask import Flask, render_template, redirect, url_for, flash
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)

# SECRET_KEY necesaria para Flask-WTF y protección CSRF
app.config["SECRET_KEY"] = "TecnoSoluciones_2026_Semana11"


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
# MÓDULO DE PRODUCTOS
# ==========================================================

@app.route("/productos")
def productos():

    productos_demo = [
        {
            "id": 1,
            "nombre": "Diseño Web Empresarial",
            "categoria": "Desarrollo Web",
            "precio": 350.00,
            "stock": 5,
            "estado": "Disponible"
        },
        {
            "id": 2,
            "nombre": "Mantenimiento de Computadores",
            "categoria": "Soporte Técnico",
            "precio": 45.00,
            "stock": 8,
            "estado": "Disponible"
        },
        {
            "id": 3,
            "nombre": "Curso de Herramientas Digitales",
            "categoria": "Capacitación",
            "precio": 60.00,
            "stock": 0,
            "estado": "Agotado"
        },
        {
            "id": 4,
            "nombre": "Consultoría Tecnológica",
            "categoria": "Consultoría",
            "precio": 90.00,
            "stock": 3,
            "estado": "Disponible"
        }
    ]

    return render_template(
        "productos.html",
        productos=productos_demo
    )


# ==========================================================
# FORMULARIO DE PRODUCTOS
# ==========================================================

@app.route("/productos/nuevo", methods=["GET", "POST"])
def formulario_producto():

    form = ProductoForm()

    if form.validate_on_submit():

        producto = {
            "nombre": form.nombre.data,
            "categoria": form.categoria.data,
            "precio": form.precio.data,
            "stock": form.stock.data
        }

        flash(
            f"Producto '{producto['nombre']}' registrado correctamente.",
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
            f"Proveedor '{proveedor['empresa']}' registrado correctamente.",
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
    app.run(debug=True)

