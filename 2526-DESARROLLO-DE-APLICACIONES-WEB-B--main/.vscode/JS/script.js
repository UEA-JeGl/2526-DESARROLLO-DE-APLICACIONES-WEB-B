// ==========================================
// SERVICIOS (ARREGLO DE OBJETOS)
// ==========================================

const servicios = [
    {
        nombre: "Desarrollo Web",
        descripcion: "Diseño y desarrollo de sitios web modernos y responsivos.",
        color: "primary"
    },
    {
        nombre: "Soporte Técnico",
        descripcion: "Mantenimiento preventivo y correctivo de equipos de cómputo.",
        color: "success"
    },
    {
        nombre: "Capacitación",
        descripcion: "Cursos y asesorías en herramientas digitales.",
        color: "warning"
    },
    {
        nombre: "Consultoría",
        descripcion: "Asesoría tecnológica para empresas y emprendedores.",
        color: "info"
    }
];

// ==========================================
// SOLICITUDES
// ==========================================

let solicitudes = [];

// ==========================================
// ELEMENTOS HTML
// ==========================================

const contenedorServicios = document.getElementById("contenedorServicios");
const listaServicios = document.getElementById("listaServicios");
const contador = document.getElementById("contador");
const formulario = document.getElementById("formServicio");
const mensaje = document.getElementById("mensaje");
const spinner = document.getElementById("spinner");

// ==========================================
// MOSTRAR SERVICIOS
// ==========================================

function mostrarServicios() {

    contenedorServicios.innerHTML = "";

    servicios.forEach(servicio => {

        contenedorServicios.innerHTML += `

        <div class="col-md-6 col-lg-3 mb-4">

            <div class="card h-100 shadow">

                <div class="card-body text-center">

                    <h5>${servicio.nombre}</h5>

                    <p>${servicio.descripcion}</p>

                    <button
                        class="btn btn-${servicio.color}"
                        onclick="abrirModal('${servicio.nombre}','${servicio.descripcion}')">

                        Ver detalles

                    </button>

                </div>

            </div>

        </div>

        `;

    });

}

// ==========================================
// MODAL
// ==========================================

function abrirModal(nombre, descripcion) {

    document.getElementById("detalleModal").innerHTML = `
        <h4>${nombre}</h4>
        <hr>
        <p>${descripcion}</p>
    `;

    const modal = new bootstrap.Modal(
        document.getElementById("modalServicio")
    );

    modal.show();

}

// ==========================================
// MOSTRAR SOLICITUDES
// ==========================================

function mostrarSolicitudes() {

    listaServicios.innerHTML = "";

    contador.textContent = solicitudes.length;

    if (solicitudes.length === 0) {

        listaServicios.innerHTML = `

        <tr>

            <td colspan="4" class="text-center text-muted">

                No existen solicitudes registradas.

            </td>

        </tr>

        `;

        return;

    }

    solicitudes.forEach((item, index) => {

        listaServicios.innerHTML += `

        <tr>

            <td>${index + 1}</td>

            <td>${item.nombre}</td>

            <td>${item.categoria}</td>

            <td>${item.descripcion}</td>

        </tr>

        `;

    });

}

// ==========================================
// VALIDACIONES
// ==========================================

formulario.addEventListener("submit", function (e) {

    e.preventDefault();

    const nombre = document.getElementById("nombre");
    const descripcion = document.getElementById("descripcion");
    const categoria = document.getElementById("categoria");

    nombre.classList.remove("is-invalid");
    descripcion.classList.remove("is-invalid");
    categoria.classList.remove("is-invalid");

    document.getElementById("errorNombre").innerHTML = "";
    document.getElementById("errorDescripcion").innerHTML = "";
    document.getElementById("errorCategoria").innerHTML = "";

    mensaje.innerHTML = "";

    if (nombre.value.trim() === "") {

        nombre.classList.add("is-invalid");
        document.getElementById("errorNombre").textContent =
            "Ingrese su nombre.";

        return;

    }

    if (descripcion.value.trim().length < 10) {

        descripcion.classList.add("is-invalid");
        document.getElementById("errorDescripcion").textContent =
            "La descripción debe tener al menos 10 caracteres.";

        return;

    }

    if (categoria.value === "") {

        categoria.classList.add("is-invalid");
        document.getElementById("errorCategoria").textContent =
            "Seleccione un servicio.";

        return;

    }

    spinner.classList.remove("d-none");

    setTimeout(() => {

        spinner.classList.add("d-none");

        solicitudes.push({

            nombre: nombre.value,
            descripcion: descripcion.value,
            categoria: categoria.value

        });

        mostrarSolicitudes();

        mensaje.innerHTML = `

        <div class="alert alert-success alert-dismissible fade show">

            <strong>Éxito.</strong>

            La solicitud fue registrada correctamente.

            <button
                type="button"
                class="btn-close"
                data-bs-dismiss="alert">
            </button>

        </div>

        `;

        formulario.reset();

    }, 1500);

});

// ==========================================
// INICIO
// ==========================================

mostrarServicios();

mostrarSolicitudes();
