// ==========================================================
// SERVICIOS DE TECNOSOLUCIONES
// ==========================================================

const servicios = [

    {
        nombre: "Desarrollo Web",
        descripcion:
            "Diseñamos sitios web modernos, funcionales y adaptables a diferentes dispositivos.",
        color: "primary"
    },

    {
        nombre: "Soporte Técnico",
        descripcion:
            "Ofrecemos mantenimiento preventivo y correctivo para equipos informáticos.",
        color: "success"
    },

    {
        nombre: "Capacitación",
        descripcion:
            "Realizamos cursos y asesorías sobre herramientas digitales y tecnología.",
        color: "warning"
    },

    {
        nombre: "Consultoría",
        descripcion:
            "Brindamos asesoramiento tecnológico para empresas y emprendedores.",
        color: "info"
    }

];


// ==========================================================
// SOLICITUDES
// ==========================================================

let solicitudes = [];


// ==========================================================
// CARGAR ELEMENTOS
// ==========================================================

const contenedorServicios =
    document.getElementById("contenedorServicios");

const listaServicios =
    document.getElementById("listaServicios");

const contador =
    document.getElementById("contador");

const formulario =
    document.getElementById("formServicio");

const mensaje =
    document.getElementById("mensaje");

const spinner =
    document.getElementById("spinner");


// ==========================================================
// MOSTRAR SERVICIOS
// ==========================================================

function mostrarServicios() {

    if (!contenedorServicios) {
        return;
    }

    contenedorServicios.innerHTML = "";

    servicios.forEach(function(servicio) {

        contenedorServicios.innerHTML += `

            <div class="col-md-6 col-lg-3">

                <div class="card shadow h-100">

                    <div class="card-body text-center">

                        <h5>

                            ${servicio.nombre}

                        </h5>

                        <p>

                            ${servicio.descripcion}

                        </p>

                        <button
                            class="btn btn-${servicio.color}"
                            onclick="mostrarDetalle(
                                '${servicio.nombre}',
                                '${servicio.descripcion}'
                            )">

                            Ver detalles

                        </button>

                    </div>

                </div>

            </div>

        `;

    });

}


// ==========================================================
// MOSTRAR DETALLE
// ==========================================================

function mostrarDetalle(nombre, descripcion) {

    alert(
        nombre +
        "\n\n" +
        descripcion
    );

}


// ==========================================================
// MOSTRAR SOLICITUDES
// ==========================================================

function mostrarSolicitudes() {

    if (!listaServicios || !contador) {
        return;
    }

    listaServicios.innerHTML = "";

    contador.textContent =
        solicitudes.length;


    if (solicitudes.length === 0) {

        listaServicios.innerHTML = `

            <tr>

                <td
                    colspan="4"
                    class="text-center text-muted">

                    No existen solicitudes registradas.

                </td>

            </tr>

        `;

        return;
    }


    solicitudes.forEach(function(item, index) {

        listaServicios.innerHTML += `

            <tr>

                <td>
                    ${index + 1}
                </td>

                <td>
                    ${item.nombre}
                </td>

                <td>
                    ${item.categoria}
                </td>

                <td>
                    ${item.descripcion}
                </td>

            </tr>

        `;

    });

}


// ==========================================================
// FORMULARIO
// ==========================================================

if (formulario) {

    formulario.addEventListener(
        "submit",
        function(evento) {

            evento.preventDefault();


            const nombre =
                document.getElementById("nombre");

            const descripcion =
                document.getElementById("descripcion");

            const categoria =
                document.getElementById("categoria");


            nombre.classList.remove(
                "is-invalid"
            );

            descripcion.classList.remove(
                "is-invalid"
            );

            categoria.classList.remove(
                "is-invalid"
            );


            document.getElementById(
                "errorNombre"
            ).textContent = "";


            document.getElementById(
                "errorDescripcion"
            ).textContent = "";


            document.getElementById(
                "errorCategoria"
            ).textContent = "";


            mensaje.innerHTML = "";


            // VALIDACIÓN DEL NOMBRE

            if (nombre.value.trim() === "") {

                nombre.classList.add(
                    "is-invalid"
                );

                document.getElementById(
                    "errorNombre"
                ).textContent =
                    "Ingrese su nombre.";

                return;
            }


            // VALIDACIÓN DE DESCRIPCIÓN

            if (
                descripcion.value.trim().length < 10
            ) {

                descripcion.classList.add(
                    "is-invalid"
                );

                document.getElementById(
                    "errorDescripcion"
                ).textContent =
                    "La descripción debe tener al menos 10 caracteres.";

                return;
            }


            // VALIDACIÓN DE CATEGORÍA

            if (categoria.value === "") {

                categoria.classList.add(
                    "is-invalid"
                );

                document.getElementById(
                    "errorCategoria"
                ).textContent =
                    "Seleccione un servicio.";

                return;
            }


            // MOSTRAR SPINNER

            if (spinner) {

                spinner.classList.remove(
                    "d-none"
                );

            }


            // SIMULACIÓN DE REGISTRO

            setTimeout(function() {

                if (spinner) {

                    spinner.classList.add(
                        "d-none"
                    );

                }


                solicitudes.push({

                    nombre:
                        nombre.value,

                    descripcion:
                        descripcion.value,

                    categoria:
                        categoria.value

                });


                mostrarSolicitudes();


                mensaje.innerHTML = `

                    <div
                        class="alert alert-success mt-3">

                        <strong>Registro exitoso.</strong>

                        La solicitud fue registrada correctamente.

                    </div>

                `;


                formulario.reset();

            }, 1000);

        }
    );

}


// ==========================================================
// INICIALIZACIÓN
// ==========================================================

mostrarServicios();

mostrarSolicitudes();
