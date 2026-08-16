from flask import Flask, render_template

# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)


# ==========================================================
# RUTA PRINCIPAL
# ==========================================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================================
# RUTA PRODUCTOS
# ==========================================================

@app.route("/productos")
def productos():

    productos_demo = [
        {
            "id": 1,
            "nombre": "Diseño Web Empresarial",
            "categoria": "Desarrollo Web",
            "precio": 350.00,
            "estado": "Disponible"
        },
        {
            "id": 2,
            "nombre": "Mantenimiento de Computadores",
            "categoria": "Soporte Técnico",
            "precio": 45.00,
            "estado": "Disponible"
        },
        {
            "id": 3,
            "nombre": "Curso de Herramientas Digitales",
            "categoria": "Capacitación",
            "precio": 60.00,
            "estado": "Disponible"
        },
        {
            "id": 4,
            "nombre": "Consultoría Tecnológica",
            "categoria": "Consultoría",
            "precio": 90.00,
            "estado": "Disponible"
        }
    ]

    return render_template(
        "productos.html",
        productos=productos_demo
    )


# ==========================================================
# RUTA CLIENTES
# ==========================================================

@app.route("/clientes")
def clientes():

    clientes_demo = [
        {
            "id": 1,
            "nombre": "Juan Pérez",
            "correo": "juan@gmail.com",
            "tipo": "Estudiante"
        },
        {
            "id": 2,
            "nombre": "María López",
            "correo": "maria@gmail.com",
            "tipo": "Emprendedor"
        },
        {
            "id": 3,
            "nombre": "Carlos Andrade",
            "correo": "carlos@gmail.com",
            "tipo": "Empresa"
        }
    ]

    return render_template(
        "clientes.html",
        clientes=clientes_demo
    )


# ==========================================================
# RUTA PROVEEDORES
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
            "estado": "Activo"
        }
    ]

    return render_template(
        "proveedores.html",
        proveedores=proveedores_demo
    )


# ==========================================================
# RUTA FACTURACIÓN
# ==========================================================

@app.route("/facturacion")
def facturacion():

    facturas_demo = [
        {
            "numero": "FAC-001",
            "cliente": "Juan Pérez",
            "fecha": "15/08/2026",
            "total": 350.00
        },
        {
            "numero": "FAC-002",
            "cliente": "María López",
            "fecha": "16/08/2026",
            "total": 90.00
        },
        {
            "numero": "FAC-003",
            "cliente": "Carlos Andrade",
            "fecha": "16/08/2026",
            "total": 60.00
        }
    ]

    return render_template(
        "facturacion.html",
        facturas=facturas_demo
    )


# ==========================================================
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)
    
