from flask import Flask, render_template

# ==========================================================
# CONFIGURACIÓN DE FLASK
# ==========================================================

app = Flask(__name__)


# ==========================================================
# PÁGINA PRINCIPAL
# ==========================================================

@app.route("/")
def inicio():

    # Variable simple
    nombre_empresa = "TecnoSoluciones"

    # Diccionario
    informacion = {
        "titulo": "Servicios Tecnológicos",
        "descripcion": "Soluciones tecnológicas para estudiantes, emprendedores y empresas.",
        "anio": 2026
    }

    # Lista de diccionarios
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
# EJECUTAR APLICACIÓN
# ==========================================================

if __name__ == "__main__":
    app.run(debug=True)

    
